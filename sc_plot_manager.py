"""
==========================================================
Plot handling methods for run_correlations.py driver file.
==========================================================

sc_plot_manager.py
Author: Teddy Rowan @ MySybil.com
Last Modified: Sept 16, 2020
Description: Helper code for run_risk_assessment.py. This code abstracts a lot of the plt setup and
 the label making which were repeated and a needless distraction from the main code base.
"""

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches

def set_defaults(plt_input):
    """
    Assign the default plot settings to the input figure.
    
    Parameters
    ----------
    plt_input :
        A matplotlib plt module
        
    Returned Variables [3]
    ----------------------
    <module> :
        The input plt input module with updated settings
    <matplotlib.figure.Figure> :
        The figure for the module
    <matplotlib.axes._subplots.AxesSubplot> :
        The axes object for the plot.
    """
    
    
    plt_input.rcParams['figure.figsize'] = (8.4, 4.2)
    # Default figure size. 2-to-1 width to height

    plt_input.rcParams['figure.subplot.left'] = 0.05
    plt_input.rcParams['figure.subplot.top'] = 0.92
    plt_input.rcParams['figure.subplot.right'] = 0.95
    # Position the chart in the figure
        
    fig_out = plt_input.figure()
    ax_out = plt_input.subplot2grid((1,1), (0,0))
    # Assign the outputs to return.
    
    ax_out.xaxis.set_ticks_position('none')
    ax_out.yaxis.set_ticks_position('none')
    # Don't print the tick dashes at the boundaries of the grid
    
    plt_input.yticks(alpha=0)
    # Don't print the ticks on the vertical axis
    
    plt_input.box(False)
    # Don't print a border around the plot
    
    plt_input.grid(color='black', linestyle='-', linewidth=1.5, alpha=0.1, zorder=0)
    # Gridline styling
    
    ax_out.xaxis.grid()
    # Only plot horizontal gridlines.

    ax_out.axhline(linewidth=1, color='black')
    # Plot the x-axis zero-line
    
    # Legend handling    
    p1patch = mpatches.Patch(color=[0, 0.75, 1.0], label="Beta to benchmark")
    p2patch = mpatches.Patch(color=[0.9, 0, 0.25], label="Negative un-CORR return /yr")
    p3patch = mpatches.Patch(color=[0, 1.0, 0.75], label="Positive un-CORR return /yr")
    legend = plt.legend(handles=[p1patch, p3patch, p2patch], framealpha=0.25, loc=0, facecolor='white', fontsize=9)
    plt_input.setp(legend.get_texts(), color='black')    
    
    return plt_input, fig_out, ax_out;


def reorient_plot(ax, n_points, y_min, y_max):
    """
    Reset the window for the plot after gradient_bar() screws up the viewer.
    
    Parameters
    ----------
    ax :
        The plot axis
    n_points :
        The number of sets of columns in the bar chart.
    y_min :
        The smallest value for a data point in the dataset
    y_max :
        The largest value for a data point in the dataset

        
    Returned Variables [nil]
    ------------------------
    
    """
    
    plt.xlim((-0.5, n_points-0.5))
    # The columns are plotted at x=0,1,2,...,n-1

    min_modifier = 0.9 if (y_min > 0) else 1.1
    max_modifier = 1.1 if (y_max > 0) else 0.9
    # Modifier values to set chart limits big enough to show the labels

    plt.ylim((y_min*min_modifier, y_max*max_modifier))
    ax.set_aspect('auto')


def customize_plot(title, x_ticks, x_tick_titles):
    """
    Graphical customization of the plot based on the data contained. Currently
    this means settings the title for the figure and overriding the tick labels.
    
    Parameters
    ----------
    title :
        <str> Title for the figure.
    x_ticks :
        The list of x_ticks for the figure.
    x_tick_titles :
        The new strings to override the current x_tick_labels        

    Returned Variables [nil]
    ------------------------
    
    """
    
    titlefont = {'fontname':'DejaVu Sans', 'fontsize':11, 'fontweight':'light'}
    plt.title(title, color='black', **titlefont)
    plt.xticks(x_ticks, x_tick_titles, color='black', fontname='DejaVu Sans', fontsize=8)
    

def create_labels(offset, ax, betas, alphas):
    """
    Create the labels above/below the bars that let us remove the y-ticks 
    and clean up the figure.
    
    Parameters
    ----------
    offset :
        <float> Standard spacing offset for the labels.
    ax :
        The plot axis.
    betas :
        A <list> of the beta/correlations for the benchmarks
    alphas :
        A <list> of the alpha/performance vs the benchmarks

    Returned Variables [nil]
    ------------------------
    
    """
    
    kwargs   = dict(fontweight='normal', fontsize=7)
    sc_blue  = [0, 0.75, 1.0]
    sc_green = [0, 1.0, 0.75]
    sc_red   = [0.9, 0, 0.25]
    
    # Generate the labels for the beta columns
    for x, y in enumerate(betas):
        lbl_text = "{:.2f}".format(y)
        
        if (y >= 0):
            ax.text(x-0.36, y+1*offset, lbl_text, color=sc_blue, **kwargs)
        else:
            ax.text(x-0.38, y-2*offset, lbl_text, color=sc_blue, **kwargs)

    # Generate the labels for the uncorrelated returns columns
    for x, y in enumerate(alphas):
        lbl_text = "{:.1f}%".format(100*y)
        
        if (y >= 0):
            """Positve Alpha"""
            if (y > 0.1): #spacing fix
                ax.text(x+0.06, y+1*offset, lbl_text, color=sc_green, **kwargs)
            else:
                ax.text(x+0.08, y+1*offset, lbl_text, color=sc_green, **kwargs)
        else:
            """Negative Alpha"""
            if (y < -0.1):
                ax.text(x+0.06, y-2*offset, lbl_text, color=sc_red, **kwargs)
            else:
                ax.text(x+0.08, y-2*offset, lbl_text, color=sc_red, **kwargs)
                
