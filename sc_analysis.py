"""
==================================================================
Helper function to abstract data analysis from run_correlations.py
==================================================================

sc_analysis.py (imported as sca)
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 22, 2020
Description: helper functions for run_correlations.py. Mainly mathematical
or analysis-based.

"""

from datetime import datetime
import time

# Find about how long a time-frame of data we're dealing with so that we can
# annualize the data. 
def calculate_data_duration(start_date):
    datenum = datetime.strptime(start_date, "%Y-%m-%d")
    timeDiff =  (time.mktime(datetime.now().timetuple())) - (time.mktime(datenum.timetuple()))
    return (timeDiff)/(60*60*24*365)
    

# Return a dictionary of the relevant min/max values for coloring and plot limits
def get_component_extrema(alphas, betas):
    ext_dict = {}
    ext_dict['min_alpha'] = min(alphas)
    ext_dict['max_alpha'] = max(alphas)
    ext_dict['min_beta'] = min(betas)
    ext_dict['max_beta'] = max(betas)
    
    # zero-bounded
    ext_dict['max'] = max(ext_dict['max_alpha'], ext_dict['max_beta'], 0) 
    ext_dict['min'] = min(ext_dict['min_alpha'], ext_dict['min_beta'], 0) 
    
    return ext_dict

# Create a dictionary of color objects for each alpha term to figure out what
# color the data should be on the figure.
def get_alpha_colors(sorted_alphas, extrema_dict):
    colors = []
    for alpha in list(sorted_alphas):
        if (alpha >= 0):
            color = [0, alpha/extrema_dict['max_alpha'], 0.25]
        else:
            color = [alpha/extrema_dict['min_alpha'], 0, 0.25]
        colors.append(color)

    return colors


# Take the daily closing prices of the trade data and then convert them to 
# percent change data + calculate the percent return.
def convert_to_percent_change(daily_data):
    percent_change = []
    last_close = 0
    for data in daily_data:
        if (last_close != 0):
            percent_change.append(float(data['close'])/last_close - 1)
        last_close = data['close']
        
    performance = daily_data[-1]['close']/daily_data[0]['close']-1
    
    return percent_change, performance
    

# Just print some basic stuff about how the simple has performed for the user.
def print_basic_return_facts(data, performance):
    print("Starting Share Price: $%.2f" % data[0]['close'])
    print("Final Share Price:    $%.2f" % data[-1]['close'])
    print("Stock Percent Return: %.2f%%" % (100*performance))
    