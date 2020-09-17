"""
============================================
Settings file for benchmark comparison tool.
============================================

correlations_settings.py
Author: Teddy Rowan @ MySybil.com
Last Modified: August 9, 2020
Description: This script stores the settings for run_correlations.py and allows the user to more
easily modify their run without having to dive into the main code. 

TODO: validate each of the settings before returning the data.
"""

def api_key():
    return 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj'
    """Communal API key, use to demo the scripts but please get your own for continued use. """
    """Sign up for free @ developer.tradier.com"""

def get_settings():
    dict = {}
    dict['API_KEY'] = api_key()
    
    dict['rfr'] = 0.002
    """ In decimal form."""
    
    dict['start_date'] = '2020-01-01'
    """ First time period to examine for the alpha/beta calculations. """

    dict['interval'] = 'daily'
    """ Interval for the alpha/beta calculations. """
    
    return dict