# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains functions to plot globally-available Natural Earth data
in order to add cultural (cities, countries, etc) and physical (lakes, rivers,
glaciers, etc) elements on plots. These use hyoga's internal shapefile plotter
which may increase speed especially for high-definition data on small domains.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as cshp
import hyoga.plot


# Natural Earth internals
# -----------------------

def feature(category=None, name=None, scale='10m', **kwargs):
    """Plot Natural Earth feature allowing a different color for the
    subject."""
    fname = cshp.natural_earth(resolution=scale, category=category, name=name)
    return hyoga.plot.shapefile(fname, **kwargs)


# Natural Earth cultural
# ----------------------

def cities(ax=None, lang=None, include=None, exclude=None, ranks=None,
           **kwargs):
    """
    Plot populated places as an annotated scatter plot.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes` (or a subclass)
        Axes used for plotting, default to current axes.
    lang : str
        Two-letters lowercase language code used to add text labels. Defaults
        to None, implying a scatter plot without text labels.
    include : list of str
        List of cities to explicitly include regardless of rank, by their
        English name. Has no effect if ranks is None.
    exclude : list of str
        List of cities to explicitly exclude regardless of rank, by their
        English name. Has no effect if ranks is None.
    ranks : list of int
        List of ranks used to filter cities by regional importance, ranging
        from 1 (more important) to 10 (less important).
    **kwargs :
        Additional keyword arguments are passed to
        :meth:`matplotlib.axes.Axes.scatter`.

    Returns
    -------
    paths : :class:`matplotlib.collections.PathCollection`
        The scatter plot path collection.
    """

    # get current axes if None provided
    ax = ax or plt.gca()

    # open shapefile data
    shp = cshp.Reader(cshp.natural_earth(
        resolution='10m', category='cultural', name='populated_places'))

    # filter by rank, include and exclude
    records = shp.records()
    if ranks is not None:
        records = [rec for rec in records if (
            rec.attributes['SCALERANK'] in ranks and
            rec.attributes['NAME_EN'] not in (exclude or []) or
            rec.attributes['NAME_EN'] in (include or []))]

    # filter intersecting geometries (this saves some time when annotating
    # cities of high rank, which are numerous, and also avoids warning-like
    # messages 'posx and posy should be finite values'.
    crs = ccrs.PlateCarree()
    axes_box = hyoga.plot.shapefile._get_extent_geometry(ax=ax, crs=crs)
    records = [r for r in records if axes_box.intersects(r.geometry)]

    # add text labels
    if lang is not None:
        for rec in records:
            ax.annotate(
                rec.attributes['NAME_'+lang.upper()],
                color=kwargs.get('color'),
                xy=(rec.geometry.x, rec.geometry.y), xytext=(3, 3),
                xycoords=crs._as_mpl_transform(ax), textcoords='offset points')

    # return scatter plot
    return ax.scatter(
        [rec.geometry.x for rec in records],
        [rec.geometry.y for rec in records],
        transform=crs, **kwargs)


def countries(edgecolor='none', facecolor='#e0e0e0', linewidth=1.0,
              subject=None, subject_facecolor='#fefee9', **kwargs):
    return feature(
        category='cultural', name='admin_0_countries',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def country_borders(edgecolor='#646464', facecolor='none', linewidth=2.0,
                    **kwargs):
    return (
        feature(
            category='cultural', name='admin_0_boundary_lines_land',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs),
        feature(
            category='cultural', name='admin_0_boundary_lines_map_units',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=0.75*linewidth,
            **kwargs))


def states(edgecolor='none', facecolor='#e0e0e0', linewidth=0.25,
           subject=None, subject_facecolor='#fefee9', **kwargs):
    return feature(
        category='cultural', name='admin_1_states_provinces',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def state_borders(edgecolor='#646464', facecolor='none', linewidth=1,
                  **kwargs):
    return feature(
        category='cultural', name='admin_1_states_provinces_lines',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


# Natural Earth physical
# ----------------------

def coastline(edgecolor='#0978ab', facecolor='none', linewidth=0.25, **kwargs):
    return feature(
        category='physical', name='coastline',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def glaciers(edgecolor='#0978ab', facecolor='#ffffff', linewidth=0.25,
             **kwargs):
    return feature(
        category='physical', name='glaciated_areas',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def lakes(edgecolor='#0978ab', facecolor='#d8f2fe', linewidth=0.25, **kwargs):
    kwargs = dict(category='physical', edgecolor=edgecolor,
                  facecolor=facecolor, linewidth=linewidth, **kwargs)
    features = feature(name='lakes', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    feature(name='lakes_europe', **kwargs),
                    feature(name='lakes_north_america', **kwargs))
    return features


def ocean(edgecolor='#0978ab', facecolor='#c6ecff', linewidth=0.25, **kwargs):
    return feature(
        category='physical', name='ocean',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def rivers(edgecolor='#0978ab', facecolor='none', linewidth=0.5, **kwargs):
    kwargs = dict(category='physical', edgecolor=edgecolor,
                  facecolor=facecolor, linewidth=linewidth, **kwargs)
    features = feature(name='rivers_lake_centerlines', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    feature(name='rivers_europe', **kwargs),
                    feature(name='rivers_north_america', **kwargs))
    return features


def graticules(edgecolor='0.25', facecolor='none', linewidth=0.1, interval=1,
               **kwargs):
    return feature(
        category='physical', name='graticules_{}'.format(interval),
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
