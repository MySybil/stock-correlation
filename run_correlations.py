"""
===========================================================================
Generate a bar chart of correlations and risk-adjusted returns for a stock.
===========================================================================

run_corrleations.py forked from run_risk_asssessment.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 22, 2020
Description: The idea is to give me a much faster and easier way to look at correlations for a single
 stock. Previously had to edit my portfolio analysis software and then create a custom portfolio.
 
"""

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
import numpy as np
import requests

import gradient_bar as gb
import sc_analysis as sca
import sc_benchmarks as scb #sb
import sc_plot_manager as scp #ph
import sc_request_manager as scr #rh
import sc_settings as scs

settings = scs.get_settings()
years_of_data = sca.calculate_data_duration(settings['start_date'])

# Print the benchmark choices and prompt the user to select one from the list.
scb.print_benchmarks()
try:
    benchmark_dict = scb.select_benchmark(int(input('Select a set of benchmarks: ')))
except ValueError:
    print("Invalid input. Using common benchmarks option.")
    benchmark_dict = scb.select_benchmark(1)

benchmark_performance = {} # dictionary of benchmarks and their performances


# Prompt the usre for what symbol they want to analyze
symbol = input("Select an underlying symbol to analyze: ").upper()
title_str = 'Benchmark Correlations for ' + symbol

# If the symbol is also being used as a benchmark, then remove the benchmark
benchmark_dict = {key:val for key, val in benchmark_dict.items() if val != symbol}


# Retrieve and analyze the Symbol Data
stock_history_data = scr.get_history(symbol, settings['interval'], settings['start_date'])
if (stock_history_data == -1):
    print("Error downloading stock data. Terminating program.")
    exit()
    
# Traverse through the stock data and calculate the daily percent changes and overall return
symbol_data, symbol_performance = sca.convert_to_percent_change(stock_history_data)
sca.print_basic_return_facts(stock_history_data, symbol_performance)


# Retrieve and analyze the Benchmark Data
benchmark_data = {}
for key in benchmark_dict:
    print("Retrieving Benchmark Data: " + key + " [" + benchmark_dict[key] + "]")
    benchmark_response = scr.get_history(benchmark_dict[key], settings['interval'], settings['start_date'])

    if (benchmark_response == -1):
        print("Error Retrieving Benchmark Data. Ignoring data for: " + key)
        continue
    
    benchmark_data[key], benchmark_performance[key] = sca.convert_to_percent_change(benchmark_response)


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


"""========================================="""
""" Everything below this is plotting stuff."""
"""========================================="""

# Determine plot color ranges -- plot green for high correlation, red for negative correlation
extrema = sca.get_component_extrema(sorted_alphas_list, sorted_betas_list)
colors = sca.get_alpha_colors(sorted_alphas_list, extrema)

# Plotting. 
plt, fig, ax1 = scp.set_defaults(plt)
bar_w = 0.5
kwargs = dict(width=bar_w-0.1, align='center', alpha=1, zorder=3)
br  = plt.bar(x_positions-bar_w/2+0.03, sorted_betas_list, **kwargs, color=[0, 0.75, 1.0])
br2 = plt.bar(x_positions+bar_w/2-0.03, sorted_alphas_list, **kwargs, color=colors)

# Overlay gradients onto the columns in the bar chart
gb.overlay_bar(br, ax1, 5, 1)
gb.overlay_bar(br2, ax1, 5, 0)

scp.reorient_plot(ax1, len(sorted_betas_list), extrema['min'], extrema['max'])
scp.customize_plot(title_str, x_positions, benchmark_ticks)

# add labels above the bars
v_offset = 0.020*(extrema['max']-extrema['min'])
scp.create_labels(v_offset, ax1, sorted_betas_list, sorted_alphas_list)
    
plt.show()    
