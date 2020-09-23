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

def calculate_data_duration(start_date):
    """ 
    Determine the timeframe of the data we're dealing with so that 
    we can annualize performance data.

    Parameters
    ----------
    start_date : 
        A date string in %Y-%m-d format (eg. 2019-01-01)

    Returned Variables [1]
    ----------------------
    <float> : 
        The duration of the dataset in years.
    
    """
    
    datenum = datetime.strptime(start_date, "%Y-%m-%d")
    # Convert the date string into a datetime object.
    
    timeDiff =  (time.mktime(datetime.now().timetuple())) - (time.mktime(datenum.timetuple()))
    # Determine the time in seconds between the start of the dataset and right now.
    
    return (timeDiff)/(60*60*24*365)
    # Return the duration of the dataset in years.


def get_component_extrema(alphas, betas):
    """ 
    Analyze the correlation data and find the extrema for each data group.

    Parameters
    ----------
    alphas : 
        <list> of alpha values for the stock relative to each benchmark
    betas :
        <list> of beta values for the stock relative to each benchmark

    Returned Variables [1]
    ----------------------
    <dict> : 
        A dictionary with keys: min_alpha, max_alpha, min_beta, max_beta,
                                min, max
        min and max are zero-bounded combinations of the two other results.
    
    """
    
    ext_dict = {}
    ext_dict['min_alpha'] = min(alphas)
    ext_dict['max_alpha'] = max(alphas)
    ext_dict['min_beta'] = min(betas)
    ext_dict['max_beta'] = max(betas)
    # Extrema for each data group
    
    ext_dict['max'] = max(ext_dict['max_alpha'], ext_dict['max_beta'], 0) 
    ext_dict['min'] = min(ext_dict['min_alpha'], ext_dict['min_beta'], 0) 
    # Zero-bounded combined extrema
    
    return ext_dict


def get_alpha_colors(sorted_alphas, extrema_dict):
    """ 
    Create a list of color objects for each alpha term to use as 
    an input to the barchart to determine the color of each column.

    Parameters
    ----------
    sorted_alphas : 
        <list> of alpha values for the stock sorted in display-order
    extrema_dict :
        <dict> returned from the get_component_extrema()

    Returned Variables [1]
    ----------------------
    <list> : 
        A list of color objects corresponding to the sorted_alphas
    
    """
    
    colors = []
    for alpha in list(sorted_alphas):
        if (alpha >= 0):
            color = [0, alpha/extrema_dict['max_alpha'], 0.25]
            # Positive alphas are green-scaled
        else:
            color = [alpha/extrema_dict['min_alpha'], 0, 0.25]
            # Negative alphas are red-scaled
        colors.append(color)

    return colors


def convert_to_percent_change(daily_data):
    """ 
    Take the daily closing prices of the trade data and then convert them to 
    percent change data + calculate the percent return.
    
    Parameters
    ----------
    daily_data : 
        json data of daily stock data returned from Tradier API

    Returned Variables [2]
    ----------------------
    <list> : 
        A list daily percent change data for the stock.
    <float> :
        The percent return of the stock over the time period.
    """
    
    percent_change = []
    last_close = 0
    for data in daily_data:
        if (last_close != 0): # Discard the first data point
            percent_change.append(float(data['close'])/last_close - 1)
        last_close = data['close']
        
    performance = daily_data[-1]['close']/daily_data[0]['close']-1
    # Calculate the percent change of the stock
    
    return percent_change, performance
    

def print_basic_return_facts(data):
    """ 
    Display some basic performance metrics about the stock.

    Parameters
    ----------
    data : 
        json data of daily stock data returned from Tradier API

    Returned Variables [nil]
    ----------------------
    
    """
    
    print("Starting Share Price: $%.2f" % data[0]['close'])
    print("Final Share Price:    $%.2f" % data[-1]['close'])
    print("Stock Percent Return: %.2f%%" % (100*(data[-1]['close']/data[0]['close']-1)))
    