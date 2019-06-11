# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Map decorations.
"""

import matplotlib.pyplot as plt


# Decoration methods
# ------------------

def add_scale_bar(ax=None, color='k', label='1km', length=1000, pad=None):
    """
    Add a horizontal bar showing map scale.

    Parameters
    ----------
    ax: GeoAxes, optional
        Axes to draw on, default to current axes.
    color: color, optional
        Color for the scale bar and annotation.
    label: string, optional
        Text label above the scale bar.
    lenght: scalar, optional
        Scale bar lenght in map units.
    pad: scalar, optional
        Padding between scale bar and axes frame in map units.
    """
    ax = ax or plt.gca()
    pad = pad or 0.25*length
    _, east, south, _ = ax.get_extent()
    ax.plot([east-pad-length, east-pad], [south+pad]*2, c=color, marker='|')
    ax.text(east-pad-0.5*length, south+pad, label+'\n',
            color=color, fontweight='bold', ha='center', va='center')
