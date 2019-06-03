# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Map annotations and GPX interface.
"""

import matplotlib.pyplot as plt


# Annotation methods
# ------------------

def _annotate_by_loc(*args, ax=None, color=None, loc='ul', offset=8, **kwargs):
    """
    Annotate by location keyword and offset.

    Parameters
    ----------
    text: string
        Annotation label text.
    xy: (scalar, scalar)
        Coordinates of the point to annotate.
    ax: Axes
        Axes to draw on, defaults to the current axes.
    loc: string
        Label location ll, lc, lr, cl, cr, ul, uc or ur.
    offset: scalar, optional
        Distance between the data point and text label.
    **kwargs:
        Additional keyword arguments are passed to annotate.
    """

    # get axes if None provided
    ax = ax or plt.gca()

    # default keyword arguments
    relpos = ({'l': 1, 'c': 0.5, 'r': 0}[loc[1]],
              {'l': 1, 'c': 0.5, 'u': 0}[loc[0]])
    arrowprops = {**dict(arrowstyle='-', color=color, relpos=relpos),
                  **kwargs.pop('arrowprops', {})}
    bbox = {**dict(pad=0, ec='none', fc='none'), **kwargs.pop('bbox', {})}

    # plot annotated waypoint
    return ax.annotate(color=color, textcoords='offset points',
                       xytext=({'l': -1, 'c': 0, 'r': 1}[loc[1]]*offset,
                               {'l': -1, 'c': 0, 'u': 1}[loc[0]]*offset),
                       ha={'l': 'right', 'c': 'center', 'r': 'left'}[loc[1]],
                       va={'l': 'top', 'c': 'center', 'u': 'bottom'}[loc[0]],
                       arrowprops=arrowprops, bbox=bbox, *args, **kwargs)
