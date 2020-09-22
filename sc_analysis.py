"""
==================================================================
Helper function to abstract data analysis from run_correlations.py
==================================================================

sc_analysis.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 22, 2020
Description: helper functions for run_correlations.py. Mainly mathematical
or analysis-based.

"""

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