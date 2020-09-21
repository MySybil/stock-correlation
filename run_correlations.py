"""
======================================================================
Generate a bar chart of correlations and relative returns for a stock.
======================================================================

run_corrleations.py forked from run_risk_asssessment.py
Author: Teddy Rowan @ MySybil.com
Last Modified: August 10, 2020
Description: The idea is to give me a much faster and easier way to look at correlations for a single
 stock. Previously had to edit my portfolio analysis software and then create a custom portfolio.

TODO: code abstraction
"""

from datetime import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
import numpy as np
import requests
import time

import sc_settings
import gradient_bar as gb
import sc_analysis as sca
import sc_benchmarks as sb
import sc_plot_manager as ph
import sc_request_manager as rh

settings = sc_settings.get_settings()
sb.print_benchmarks()
try:
    benchmark_dict = sb.select_benchmark(int(input('Select a set of benchmarks: ')))
except ValueError:
    print("Invalid input. Using common benchmarks option.")
    benchmark_dict = sb.select_benchmark(1)

benchmark_performance = {} # dictionary of benchmarks and their performances


# Prompt the usre for what symbol they want to analyze
symbol = input("Select an underlying symbol to analyze: ").upper()
title_str = 'Benchmark Correlations for ' + symbol

# If the symbol is also being used as a benchmark, then remove the benchmark
benchmark_dict = {key:val for key, val in benchmark_dict.items() if val != symbol}

# Calculate how long the time period we're looking at is so we can annualize alpha.
datenum = datetime.strptime(settings['start_date'], "%Y-%m-%d")
timeDiff =  (time.mktime(datetime.now().timetuple())) - (time.mktime(datenum.timetuple()))
years_of_data = (timeDiff)/(60*60*24*365)


# Retrieve and analyze the Symbol Data
stock_history_data = rh.get_history(symbol, settings['interval'], settings['start_date'])
if (stock_history_data == -1):
    print("Error downloading stock data. Terminating program.")
    exit()
    
# Traverse through the stock data and calculate the daily percent changes and overall return
percent_change_data = []
last_close = 0
for data in stock_history_data:
    if (last_close != 0):
        percent_change_data.append(float(data['close'])/last_close - 1)
    last_close = data['close']

symbol_performance = stock_history_data[-1]['close']/stock_history_data[0]['close'] - 1 #
symbol_data = percent_change_data
portfolio_value = stock_history_data[-1]['close']       #last_price * quantity
portfolio_start_value = stock_history_data[0]['close']  #first_price * quantity

print("Starting Share Price: $%.2f" % portfolio_start_value)
print("Final Share Price:    $%.2f" % portfolio_value)
print("Stock Percent Return: %.2f%%" % (100*symbol_performance))


# Retrieve and analyze the Benchmark Data
benchmark_data = {}
for key in benchmark_dict:
    print("Retrieving Benchmark Data: " + key + " [" + benchmark_dict[key] + "]")
    benchmark_response = rh.get_history(benchmark_dict[key], settings['interval'], settings['start_date'])

    if (benchmark_response == -1):
        print("Error Retrieving Benchmark Data. Ignoring data for: " + key)
        continue
    
    benchmark_percent_change_data = []
    last_close = 0
    for data in benchmark_response:
        if (last_close != 0):
            benchmark_percent_change_data.append(float(data['close'])/last_close - 1)
        last_close = data['close']

    benchmark_performance[key] = benchmark_response[-1]['close']/benchmark_response[0]['close'] - 1
    benchmark_data[key] = benchmark_percent_change_data


# Calcuate the correlations and risk-adjusted performance of the stock vs each benchmark
alpha_values = {} # the alpha for each individual benchmark
beta_values = {} # the beta for each individual benchmark
annu_port = pow((1+symbol_performance), 1/years_of_data)-1 # annualized portfolio return
    
for benchmark_key in benchmark_data:
    result_mat = np.cov(np.stack((symbol_data, benchmark_data[benchmark_key]), axis = 0))
    annu_market = pow((1+benchmark_performance[benchmark_key]), 1/years_of_data)-1 # annualized benchmark return
        
    beta = result_mat[1][0]/result_mat[1][1]
    alpha = (pow((1+symbol_performance), 1/years_of_data)-1) - settings['rfr'] - beta*(annu_market - settings['rfr'])
    
    alpha_values[benchmark_key] = alpha
    beta_values[benchmark_key] = beta


# Sort the betas so that we can bar chart them in order. 
sorted_correlations = dict(sorted(beta_values.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
benchmark_ticks = sorted_correlations.keys()
x_positions = np.arange(len(benchmark_ticks)) # get 0 through N-1 positions for plotting
sorted_betas_list = sorted_correlations.values()

# Take the sort order from the betas and sort the alphas to match
sorted_alphas_list = []
for key in sorted_correlations:
    sorted_alphas_list.append(alpha_values[key])


## Everything below this is plotting stuff.
plt, fig, ax1 = ph.set_defaults(plt)

# Determine plot color ranges -- plot green for high correlation, red for negative correlation
extrema =  sca.get_component_extrema(sorted_alphas_list, sorted_betas_list)
colors = []
for alpha in list(sorted_alphas_list):
    if (alpha >= 0):
        color = [0, alpha/extrema['max_alpha'], 0.25]
    else:
        color = [alpha/extrema['min_alpha'], 0, 0.25]
    colors.append(color)
    
# Plotting. 
bar_w = 0.5
kwargs = dict(width=bar_w-0.1, align='center', alpha=1, zorder=3)
br  = plt.bar(x_positions-bar_w/2+0.03, sorted_betas_list, **kwargs, color=[0, 0.75, 1.0])
br2 = plt.bar(x_positions+bar_w/2-0.03, sorted_alphas_list, **kwargs, color=colors)

# Overlay gradients onto the columns in the bar chart
gb.overlay_bar(br, ax1, 5, 1)
gb.overlay_bar(br2, ax1, 5, 0)

# Re-orient after gradient fucks that up.
plt.xlim((-0.5, len(sorted_betas_list)-0.5))
plt.ylim((extrema['min']*1.1, extrema['max']*1.1))
ax1.set_aspect('auto')

titlefont = {'fontname':'DejaVu Sans', 'fontsize':11, 'fontweight':'light'}
plt.title(title_str, color='black', **titlefont)
plt.xticks(x_positions, benchmark_ticks, color='black', fontname='DejaVu Sans', fontsize=8)


# add labels above the bars
v_offset = 0.020*(extrema['max']-extrema['min'])
ph.create_labels(v_offset, ax1, sorted_betas_list, sorted_alphas_list)
    
plt.show()    
