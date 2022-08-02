# Copyright (c) 2019, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Map annotations and GPX interface.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# Annotation methods
# ------------------

def annotate_by_compass(*args, ax=None, color=None, point='ne', offset=8,
                        **kwargs):
    """
    Annotate by compass point and offset.

    Parameters
    ----------
    text: string
        Annotation label text.
    xy: (scalar, scalar)
        Coordinates of the point to annotate.
    ax: Axes
        Axes to draw on, defaults to the current axes.
    point: 'n', 'e', 's', 'w', 'ne', 'nw', 'se', or 'sw'.
        Compass point giving the annotation direction.
    offset: scalar, optional
        Distance between the data point and text label.
    **kwargs:
        Additional keyword arguments are passed to annotate.
    """

    # get axes if None provided
    ax = ax or plt.gca()

    # check location keyword validity
    valid_points = 'n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'
    if point not in valid_points:
        raise ValueError('Unrecognized compass point {!r} not in {}.'
                         .format(point, valid_points))

    # text label position and relative anchor for the text box
    xpos = 1 if 'e' in point else -1 if 'w' in point else 0
    ypos = 1 if 'n' in point else -1 if 's' in point else 0
    offset = offset / (xpos*xpos+ypos*ypos)**0.5
    xytext = xpos*offset, ypos*offset
    relpos = (1-xpos)/2, (1-ypos)/2

    # text alignement
    halign = 'left' if 'e' in point else 'right' if 'w' in point else 'center'
    valign = 'bottom' if 'n' in point else 'top' if 's' in point else 'center'

    # default style; use transparent bbox for positioning
    arrowprops = {**dict(arrowstyle='-', color=color, relpos=relpos),
                  **kwargs.pop('arrowprops', {})}
    bbox = {**dict(pad=0, ec='none', fc='none'), **kwargs.pop('bbox', {})}

    # plot annotated waypoint
    return ax.annotate(arrowprops=arrowprops, bbox=bbox, color=color,
                       textcoords='offset points', xytext=xytext,
                       ha=halign, va=valign, *args, **kwargs)


def annotate_location(location, ax=None, color=None, marker='o', text='',
                      **kwargs):
    """
    Mark and annotate a geographic location.

    Parameters
    ----------
    location: object
        A location object with longitude and latitude attributes, and by
        default a name (see text). This could be a waypoint from a GPX file.
    ax: GeoAxes, optional
        Axes used for plotting. Default to current axes.
    color:
        Color for plot and annotation.
    marker:
        Marker for plot.
    text: string, optional.
        Label text. Can be a format string with custom location object
        attribute in curly brackets, for isntance '{location.name}'.
    **kwargs:
        Additional keyword arguments are passed to annotate_by_compass.
    """

    # get axes if None provided
    ax = ax or plt.gca()

    # reproject waypoint coordinates
    crs = ccrs.PlateCarree()
    coords = location.longitude, location.latitude
    coords = ax.projection.transform_point(*coords, crs)

    # plot annotated waypoint and stop here if text is empty or (still) None
    line = ax.plot(*coords, color=color, marker=marker)
    if not text:
        return line

    # otherwise format text against location attributes and add annotation
    text = text.format(location=location)
    return annotate_by_compass(text, coords, ax=ax, color=color, **kwargs)
