"""
===========================================================
Request handling for benchmark correlation comparison tool.
===========================================================

sc_request_manager.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 26, 2020
Description: this script handles the requests for correlation scripts.

"""

import requests
import sc_settings

root_url = 'https://sandbox.tradier.com/v1/markets'

def get_history(symbol, interval, start_date):
    """ 
    GET request to the Tradier API to download daily stock data
    for the requested symbol (either input or benchmark). Verify
    the data is valid and then return the json response.
    
    Parameters
    ----------
    symbol : 
        Stock ticker for the 
    interval : 
        'daily', 'weekly', or 'monthly'
    start_date : 
        A date string in %Y-%m-d format (eg. 2019-01-01)


    Returned Variables [1]
    ----------------------
    <list> : 
        A list of dicts for each trading interval. Lists have keys:
        'date', 'open', 'high', 'low', 'close'
        
    """

    try:
        response = requests.get(root_url + '/history',
            params={'symbol': symbol, 
                    'interval': interval, 
                    'start': start_date},
            headers={'Authorization': sc_settings.api_key(), 
                     'Accept': 'application/json'}
        ).json()
    
        json_data = response['history']['day']
        return json_data
    except TypeError:
        return -1
