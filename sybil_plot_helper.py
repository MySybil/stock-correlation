"""
==========================================================
Plot handling methods for run_correlations.py driver file.
==========================================================

sybil_plot_helper.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 16, 2020
Description: Helper code for run_risk_assessment.py. This code abstracts a lot of the plt setup and
 the label making which were repeated and a needless distraction from the main code base.
"""

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches

# Assign the default plot settings for the figure.
def set_defaults(plt_input):
    plt_input.rcParams['figure.figsize'] = (8.4, 4.2)
    plt_input.rcParams['figure.subplot.left'] = 0.05
    plt_input.rcParams['figure.subplot.top'] = 0.92
    plt_input.rcParams['figure.subplot.right'] = 0.95
    plt_input.rcParams["axes.linewidth"] = 0.75
    plt_input.rcParams["axes.edgecolor"] = "0.0"
    
    fig_out = plt_input.figure()
    ax_out = plt_input.subplot2grid((1,1), (0,0))
    
    ax_out.xaxis.set_ticks_position('none')
    ax_out.yaxis.set_ticks_position('none')
    
    plt_input.yticks(alpha=0)
    plt_input.box(False)
    plt_input.grid(color='black', linestyle='-', linewidth=1.5, alpha=0.1, zorder=0)
    ax_out.xaxis.grid() #only plot horizontal gridlines.
    
    p1patch = mpatches.Patch(color=[0, 0.75, 1.0], label="Benchmark Beta")
    p2patch = mpatches.Patch(color=[0.9, 0, 0.25], label="Negative uncorrelated return")
    p3patch = mpatches.Patch(color=[0, 1.0, 0.75], label="Positive uncorrelated return")
    legend = plt.legend(handles=[p1patch, p3patch, p2patch], framealpha=0.25, loc=0, facecolor='white', fontsize=9)
    plt_input.setp(legend.get_texts(), color='black')
        
    textboxfont = {'fontname':'DejaVu Sans', 'fontsize':10, 'fontweight':'light'}
    props = dict(boxstyle='square', facecolor='none', alpha=0, edgecolor='none')
    ax_out.text(0.90, 1.05, 'MySybil.com', transform=ax_out.transAxes, verticalalignment='top', bbox=props, **textboxfont, color='red')
    
    ax_out.axhline(linewidth=1, color='black')
        
    return plt_input, fig_out, ax_out;

# Create the labels above/below the bars that let us remove the y-ticks and clean up the figure
def create_labels(offset, ax, betas, alphas):
    kwargs = dict(fontweight='normal', fontsize=7)
    
    # Generate the labels for the beta columns
    for i, v in enumerate(betas):
        lbl_text = "{:.2f}".format(v)
        
        if (v >= 0):
            ax.text(i-0.36, v+1*offset, lbl_text, color=[0, 0.75, 1.0], **kwargs)
        else:
            ax.text(i-0.38, v-2*offset, lbl_text, color=[0, 0.75, 1.0], **kwargs)

    # Generate the labels for the uncorrelated returns columns
    for i, v in enumerate(alphas):
        lbl_text = "{:.1f}%".format(100*v)
        
        if (v >= 0):
            if (v > 0.1): #spacing fix
                ax.text(i+0.06, v+1*offset, lbl_text, color=[0, 1.0, 0.75], **kwargs)
            else:
                ax.text(i+0.08, v+1*offset, lbl_text, color=[0, 1.0, 0.75], **kwargs)
        else:
            if (v < -0.1):
                ax.text(i+0.06, v-2*offset, lbl_text, color=[0.9, 0, 0.25], **kwargs)
            else:
                ax.text(i+0.08, v-2*offset, lbl_text, color=[0.9, 0, 0.25], **kwargs)
                
                