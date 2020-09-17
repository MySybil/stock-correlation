"""
========================
Bar chart with gradients
========================

Matplotlib does not natively support gradients. However, we can emulate a
gradient-filled rectangle by an `.AxesImage` of the right size and coloring.

In particular, we use a colormap to generate the actual colors. It is then
sufficient to define the underlying values on the corners of the image and
let bicubic interpolation fill out the area. We define the gradient direction
by a unit vector *v*. The values at the corners are then obtained by the
lengths of the projections of the corner vectors on *v*.

A similar approach can be used to create a gradient background for an axes.
In that case, it is helpful to uses Axes coordinates (``extent=(0, 1, 0, 1),
transform=ax.transAxes``) to be independent of the data coordinates.

# Source: https://matplotlib.org/3.2.0/gallery/lines_bars_and_markers/gradient_bar.html

CHANGELOG:
    - Added overlay_bar() designed to overlay a 0.6 alpha gradient over
      bar charts to give them more pop. The gradient in overlay_bar()
      also has a cmap dependent on whether the bar it is overlaying
      would be blue, green, or red. 
    - Deleted demo code. 
"""
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)


def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, interpolation='bicubic',
                   vmin=0, vmax=1, **kwargs)
    return im


def gradient_bar(ax, x, y, width=0.5, bottom=0):
    for left, top in zip(x, y):
        right = left + width
        gradient_image(ax, 
                       extent=(left, right, bottom, top),
                       cmap=plt.cm.Blues_r, 
                       cmap_range=(0, 0.8))

def overlay_bar(br, ax, z, is_beta):
    """ 
    Generate a 0.6 alpha gradient on-top of a the entries
    in a bar chart.

    Parameters
    ----------
    br : 
        The returned data from a plt.bar chart.
    ax : Axes
        The axes to draw on.
    z : 
        The z-order to draw the overlay at.
    is_beta:
        This function is used to draw overlays on columns 
        both for two different types of data (alpha/beta). 
        The is_beta parameter allows for the cmap of the 
        gradient to be set independently for the two
        types of data.
    """
    for b in br:
        w,h = b.get_width(), b.get_height()
        x0, y0 = b.xy       # lower left vertex
        
        if (is_beta):
            c_scheme = plt.cm.Blues_r
        elif (h < 0):
            c_scheme = plt.cm.Reds_r
        else:
            c_scheme = plt.cm.Greens_r
        
        gradient_image(ax, 
                       extent=(x0, x0+w, y0, y0+h), 
                       cmap=c_scheme,
                       cmap_range=(0.5, 0.95), 
                       alpha=0.6, 
                       zorder=z)
