"""
=============================================================
Dictionaries of custom sets of benchmarks to measure against.
=============================================================

sc_benchmarks.py
Author: Teddy Rowan @ MySybil.com
Created: December 31, 2019
Description: Helper code for run_risk_assessment.py. This code allows the user to set the benchmarks they want to compare to without turning the main code base into a disgusting mess.

-------------------------------------------
See a list of many examples at the bottom.
"""

# 0
def benchmarks_custom(): 
    output = {}
    # Add your additional benchmarks here (order independent)
    # output['NAME'] = 'SYMBOL'
    output['NASDAQ'] = 'QQQ'
    return output

def select_benchmark(num):
    if (num == 0):
        return benchmarks_custom()
    elif num == 1:
        return benchmarks_common()
    elif num == 2:
        return benchmarks_global()
    elif num == 3:
        return benchmarks_resources()
    else:
        print("Invalid selection. Using common benchmarks option.")
        return benchmarks_common()

def print_benchmarks():
    a = {'0':'Custom User Benchmarks', 
         '1':'Common Benchmarks (SP500, NASDAQ, Energy, etc.)',
         '2':'Global Benchmarks (SP500, Canada, China, UK, etc.)',
         '3':'Common Resources  (Energy, Gold, Timber, etc.)'}

    print("Available benchmarks for comparison: ")
    for key in a:
        print(key + ": " + a[key])

# 1
def benchmarks_common():
    output = {}
    output['SP500'] = 'SPY'
    output['NASDAQ'] = 'QQQ'
    output['Energy'] = 'USO'
    output['Gold'] = 'GLD'
    output['China'] = 'MCHI' 
    output['REITs'] = 'VNQ'    
    output['Bitcoin'] = 'GBTC'
    output['MJ'] = 'MJ'
    
    return output

# 2
def benchmarks_global():
    output = {}
    output['SP500'] = 'SPY'
    output['Canada'] = 'EWC' #HEWC is the hedged version
    output['China'] = 'MCHI' 
    output['UK'] = 'EWU'
    output['Saudi Arabia'] = 'KSA'
    output['Turkey'] = 'TUR'
    
    return output

# 3
def benchmarks_resources():
    output = {}
    output['Energy'] = 'USO'
    output['Gold'] = 'GLD'
    output['REITs'] = 'VNQ'
    output['Timber'] = 'WOOD'
    
    return output

"""
Pre-made for reference. 
    output['Bonds'] = 'BND' # potentially broken?
    output['Bitcoin'] = 'GBTC' #GBTC beta 1Y weekly is 1.01 right now
    output['Canada'] = 'EWC'
    output['China'] = 'MCHI' 
    output['DJIX'] = 'IYY'
    output['Energy'] = 'USO'
    output['Gold'] = 'GLD'
    output['MJ'] = 'MJ'    
    output['NASDAQ'] = 'QQQ'
    output['REITs'] = 'VNQ'    
    output['PREF\nShares'] = 'PFF'
    output['Saudi Arabia'] = 'KSA'
    output['SP500'] = 'SPY'
    output['Timber'] = 'WOOD'
    output['Turkey'] = 'TUR'
    output['UK'] = 'EWU'
    output['USD'] = 'UUP' # Global Weighted US Dollar Strength
"""