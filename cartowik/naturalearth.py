# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Natural Earth plotting tools.
"""

import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import cartopy.crs as ccrs
import cartopy.io.shapereader as cshp


# Natural Earth internals
# -----------------------

def add_feature(category=None, name=None, scale='10m', **kwargs):
    """Plot Natural Earth feature allowing a different color for the
    subject."""
    fname = cshp.natural_earth(resolution=scale, category=category, name=name)
    return add_shapefile(fname, **kwargs)


def add_shapefile(filename, ax=None, crs=None, subject=None, **kwargs):
    """Plot shapefile geometries allowing a different color for the subject."""

    # get current axes if None provided
    ax = ax or plt.gca()

    # prepare axes extent geometry
    crs = crs or ccrs.PlateCarree()
    axes_box = _get_extent_geometry(ax=ax, crs=crs)

    # open shapefile data
    shp = cshp.Reader(filename)

    # separate subject and default kwargs
    subject_kw = {k[8:]: kwargs[k] for k in kwargs if k.startswith('subject_')}
    context_kw = {k: kwargs[k] for k in kwargs if not k.startswith('subject_')}

    # find intersecting geometries
    subject_geometries = []
    context_geometries = []
    for rec in shp.records():
        if rec.geometry is not None and axes_box.intersects(rec.geometry):
            name = rec.attributes.get('name', rec.attributes.get('NAME', None))
            if subject is not None and name == subject and \
                    rec.geometry not in subject_geometries:
                subject_geometries.append(rec.geometry)
            elif rec.geometry not in context_geometries:
                context_geometries.append(rec.geometry)

    # plot interseecting geometries
    return (ax.add_geometries(context_geometries, crs, **context_kw),
            ax.add_geometries(subject_geometries, crs, **subject_kw))


def _get_extent_geometry(ax=None, crs=None):
    """Return axes extent as shapely geometry."""
    ax = ax or plt.gca()
    west, east, south, north = ax.get_extent(crs=crs)
    return sgeom.box(west, south, east, north)


# Natural Earth cultural
# ----------------------

def add_cities(ax=None, lang=None, include=None, exclude=None, ranks=None,
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
    axes_box = _get_extent_geometry(ax=ax, crs=crs)
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


def add_countries(edgecolor='none', facecolor='#e0e0e0', linewidth=1.0,
                  subject=None, subject_facecolor='#fefee9', **kwargs):
    return add_feature(
        category='cultural', name='admin_0_countries',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def add_country_borders(edgecolor='#646464', facecolor='none', linewidth=2.0,
                        **kwargs):
    return (
        add_feature(
            category='cultural', name='admin_0_boundary_lines_land',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs),
        add_feature(
            category='cultural', name='admin_0_boundary_lines_map_units',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=0.75*linewidth,
            **kwargs))


def add_states(edgecolor='none', facecolor='#e0e0e0', linewidth=0.25,
               subject=None, subject_facecolor='#fefee9', **kwargs):
    return add_feature(
        category='cultural', name='admin_1_states_provinces',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def add_state_borders(edgecolor='#646464', facecolor='none', linewidth=1.0,
                      **kwargs):
    return add_feature(
        category='cultural', name='admin_1_states_provinces_lines',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


# Natural Earth physical
# ----------------------

def add_coastline(edgecolor='#0978ab', facecolor='none', linewidth=0.25,
                  **kwargs):
    return add_feature(
        category='physical', name='coastline',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_glaciers(edgecolor='#0978ab', facecolor='#ffffff', linewidth=0.25,
                 **kwargs):
    return add_feature(
        category='physical', name='glaciated_areas',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_lakes(edgecolor='#0978ab', facecolor='#d8f2fe', linewidth=0.25,
              **kwargs):
    kwargs = dict(category='physical', edgecolor=edgecolor,
                  facecolor=facecolor, linewidth=linewidth, **kwargs)
    features = add_feature(name='lakes', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    add_feature(name='lakes_europe', **kwargs),
                    add_feature(name='lakes_north_america', **kwargs))
    return features


def add_ocean(edgecolor='#0978ab', facecolor='#c6ecff', linewidth=0.25,
              **kwargs):
    return add_feature(
        category='physical', name='ocean',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_rivers(edgecolor='#0978ab', facecolor='none', linewidth=0.5,
               **kwargs):
    kwargs = dict(category='physical', edgecolor=edgecolor,
                  facecolor=facecolor, linewidth=linewidth, **kwargs)
    features = add_feature(name='rivers_lake_centerlines', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    add_feature(name='rivers_europe', **kwargs),
                    add_feature(name='rivers_north_america', **kwargs))
    return features


def add_graticules(edgecolor='0.25', facecolor='none', linewidth=0.1,
                   interval=1, **kwargs):
    return add_feature(
        category='physical', name='graticules_{}'.format(interval),
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
