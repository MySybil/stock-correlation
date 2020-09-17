"""
===========================================================
Request handling for benchmark correlation comparison tool.
===========================================================

sybil_request_helper.py
Author: Teddy Rowan @ MySybil.com
Last Modified: August 10, 2020
Description: this script handles the requests for correlation scripts.

"""

import requests
import correlation_settings

root_url = 'https://sandbox.tradier.com/v1/markets'

# Download the historic trading data for the symbol
def get_history(symbol, interval, start_date):
    response = requests.get(root_url + '/history',
        params={'symbol': symbol, 
                'interval': interval, 
                'start': start_date},
        headers={'Authorization': correlation_settings.api_key(), 
                 'Accept': 'application/json'}
    )
    json_response = response.json()

    try:
        json_data = json_response['history']['day']
        return json_data
    except TypeError:
        return -1
