# Copyright (c) 2019--2020, Julien Seguinot (juseg.github.io)
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


def add_subfig_label(*args, ax=None, loc='nw', offset=8, **kwargs):
    """Add a subfigure label positioned by compass point. Defaults to an upper
    left (nw) corner in bold font.

    Parameters
    ----------
    text: string
        Subfigure label text.
    ax: Axes
        Axes to draw on, defaults to the current axes.
    loc: 'n', 'e', 's', 'w', 'ne', 'nw', 'se', or 'sw'.
        Compass point giving the label position.
    offset: scalar, optional
        Distance between the data point and text label.
    **kwargs:
        Additional keyword arguments are passed to annotate.
    """

    # get axes if None provided
    ax = ax or plt.gca()

    # check location keyword validity
    valid_locs = 'n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'
    if loc not in valid_locs:
        raise ValueError('Unrecognized location {!r} not in {}.'
                         .format(loc, valid_locs))

    # text label position and offset relative to axes corner
    xpos = 1 if 'e' in loc else 0 if 'w' in loc else 0.5
    ypos = 1 if 'n' in loc else 0 if 's' in loc else 0.5
    xshift = 1-2*xpos
    yshift = 1-2*ypos
    offset = offset / (xshift*xshift+yshift*yshift)**0.5
    xytext = xshift*offset, yshift*offset

    # text alignement (opposite from annotations)
    halign = 'left' if 'w' in loc else 'right' if 'e' in loc else 'center'
    valign = 'bottom' if 's' in loc else 'top' if 'n' in loc else 'center'

    # add annotation
    return ax.annotate(fontweight=kwargs.pop('fontweight', 'bold'),
                       xy=(xpos, ypos), xytext=xytext,
                       textcoords='offset points', xycoords='axes fraction',
                       ha=halign, va=valign, *args, **kwargs)
