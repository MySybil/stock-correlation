"""
==================================================================
Helper function to abstract data analysis from run_correlations.py
==================================================================

sc_analysis.py.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 21, 2020
Description: The idea is to give me a much faster and easier way to look at correlations for a single
 stock. Previously had to edit my portfolio analysis software and then create a custom portfolio.

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
    