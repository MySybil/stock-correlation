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
import sc_benchmarks as scb
import sc_plot_manager as scp
import sc_request_manager as scr
import sc_settings as scs

settings = scs.get_settings()
# Retrieve the compile time settings for the tool

years_of_data = sca.calculate_data_duration(settings['start_date'])
# Find out the time-length of the data so we can annualize numbers

scb.print_benchmarks()
# Print the benchmark choices and descriptions for the user

# Prompt the user to select a benchmark and error catch to the default benchmark
try:
    benchmark_dict = scb.select_benchmark(int(input('Select a set of benchmarks: ')))
except ValueError:
    print("Invalid input. Using common benchmarks option.")
    benchmark_dict = scb.select_benchmark(1)


symbol = input("Select an underlying symbol to analyze: ").upper()
# Prompt the user to choose a stock to analyze.

benchmark_dict = {key:val for key, val in benchmark_dict.items() if val != symbol}
# If the symbol is also being used as a benchmark, then remove the benchmark

stock_history_data = scr.get_history(symbol, settings['interval'], settings['start_date'])
# Retrieve and analyze the price history for the symbol data

# Validate the downloaded data
if (stock_history_data == -1):
    print("Error downloading stock data. Terminating program.")
    exit()
    

symbol_data, symbol_performance = sca.convert_to_percent_change(stock_history_data)
# Traverse the stock data and calculate the daily percent changes and overall return

sca.print_basic_return_facts(stock_history_data)
# Display some basic details about the stock's performance


# Retrieve and analyze the Benchmark Data
benchmark_data = {}
benchmark_performance = {}
for key in benchmark_dict:
    print("Retrieving Benchmark Data: " + key + " [" + benchmark_dict[key] + "]")
    benchmark_response = scr.get_history(benchmark_dict[key], settings['interval'], settings['start_date'])
    # Retrieve and analyze the price history for the benchmark

    # Validate the downloaded data
    if (benchmark_response == -1):
        print("Error Retrieving Benchmark Data. Ignoring data for: " + key)
        continue
    
    benchmark_data[key], benchmark_performance[key] = sca.convert_to_percent_change(benchmark_response)
    # Convert the daily close data to percent change data


alpha_values = {}
beta_values = {}
# Dictionaries to store the CAPM results

annu_port = pow((1+symbol_performance), 1/years_of_data)-1
# Calculate the annualized portfolio return

# Calcuate the correlations and risk-adjusted performance of the stock vs each benchmark    
for benchmark_key in benchmark_data:
    annu_market = pow((1+benchmark_performance[benchmark_key]), 1/years_of_data)-1
    # Calculate the annualized return of the benchmark

    result_mat = np.cov(np.stack((symbol_data, benchmark_data[benchmark_key]), axis = 0))
    # Generate a covariance matrix between the symbol and the benchmark
    
    beta_values[benchmark_key] = result_mat[1][0]/result_mat[1][1]
    # Calculate the beta from the covariance matrix
    
    alpha_values[benchmark_key] = (pow((1+symbol_performance), 1/years_of_data)-1) - settings['rfr'] - beta_values[benchmark_key]*(annu_market - settings['rfr'])
    # Calculate the alpha from the performance and beta result
    

sorted_correlations = dict(sorted(beta_values.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
# Sort the betas so that we can plot the benchmarks in order of correlation

benchmark_ticks = sorted_correlations.keys()
# Create a list of the tick values in plot-order

x_positions = np.arange(len(benchmark_ticks))
# Array of 0 to N-1 as positions for plotting the columns

sorted_betas_list = sorted_correlations.values()
# Extract the beta values for the chart

# Take the sort order from the betas and sort the alphas to match
sorted_alphas_list = []
for key in sorted_correlations:
    sorted_alphas_list.append(alpha_values[key])


"""
==========================================
 Everything below this is plotting stuff.
==========================================
"""

extrema = sca.get_component_extrema(sorted_alphas_list, sorted_betas_list)
# Determine the (zero-constrained) extrema we will need to know

colors = sca.get_alpha_colors(sorted_alphas_list, extrema)
# Assign a color to each column to be plotted

plt, fig, ax1 = scp.set_defaults(plt)
# Default plot design / settings

bar_w = 0.5
# Column width for barchart

kwargs = dict(width=bar_w-0.1, align='center', alpha=1, zorder=3)
# Shared plot settings between alpha/beta columns

br  = plt.bar(x_positions-bar_w/2+0.03, sorted_betas_list, **kwargs, color=[0, 0.75, 1.0])
# Plot the beta columns

br2 = plt.bar(x_positions+bar_w/2-0.03, sorted_alphas_list, **kwargs, color=colors)
# Plot the alpha columns

gb.overlay_bar(br, ax1, 5, True)
# Overlay a blue-gradient onto the beta columns

gb.overlay_bar(br2, ax1, 5, False)
# Overlay custom red/green gradients on the alpha columns

scp.reorient_plot(ax1, len(sorted_betas_list), extrema['min'], extrema['max'])
# After generating gradients the plot window gets screwed up badly

title_str = 'Benchmark Correlations for ' + symbol
scp.customize_plot(title_str, x_positions, benchmark_ticks)
# Override the x-ticklabels with benchmark names. Add a title to the figure.

v_offset = 0.020*(extrema['max']-extrema['min'])
# Vertical offset for the labels above/below the columns

scp.create_labels(v_offset, ax1, sorted_betas_list, sorted_alphas_list)
# Create the labels above/below the columns
    
plt.show()    
