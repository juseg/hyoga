# Copyright (c) 2018--2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
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
    add_shapefile(fname, **kwargs)


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
    default_kw = {k: kwargs[k] for k in kwargs if not k.startswith('subject_')}

    # add intersecting geometries
    for rec in shp.records():
        if rec.geometry is not None and axes_box.intersects(rec.geometry):
            name = rec.attributes.get('name', rec.attributes.get('NAME', None))
            props = (subject_kw if subject is not None and name == subject
                     else default_kw)
            ax.add_geometries(rec.geometry, crs, **props)


def _get_extent_geometry(ax=None, crs=None):
    """Return axes extent as shapely geometry."""
    ax = ax or plt.gca()
    west, east, south, north = ax.get_extent(crs=crs)
    return sgeom.box(west, south, east, north)


# Natural Earth cultural
# ----------------------

def add_countries(edgecolor='none', facecolor='#e0e0e0', linewidth=1.0,
                  subject=None, subject_facecolor='#fefee9', **kwargs):
    add_feature(
        category='cultural', name='admin_0_countries',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def add_country_borders(edgecolor='#646464', facecolor='none', linewidth=2.0,
                        **kwargs):
    add_feature(
        category='cultural', name='admin_0_boundary_lines_land',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
    add_feature(
        category='cultural', name='admin_0_boundary_lines_map_units',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=0.75*linewidth,
        **kwargs)


def add_states(edgecolor='none', facecolor='#e0e0e0', linewidth=0.25,
               subject=None, subject_facecolor='#fefee9', **kwargs):
    add_feature(
        category='cultural', name='admin_1_states_provinces',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        subject=subject, subject_facecolor=subject_facecolor, **kwargs)


def add_state_borders(edgecolor='#646464', facecolor='none', linewidth=1.0,
                      **kwargs):
    add_feature(
        category='cultural', name='admin_1_states_provinces_lines',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


# Natural Earth physical
# ----------------------

def add_coastline(edgecolor='#0978ab', facecolor='none', linewidth=0.25,
                  **kwargs):
    add_feature(
        category='physical', name='coastline',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_glaciers(edgecolor='#0978ab', facecolor='#ffffff', linewidth=0.25,
                 **kwargs):
    add_feature(
        category='physical', name='glaciated_areas',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_lakes(edgecolor='#0978ab', facecolor='#d8f2fe', linewidth=0.25,
              **kwargs):
    add_feature(
        category='physical', name='lakes',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
    if 'scale' in kwargs and 'scale' == '10m':
        add_feature(
            category='physical', name='lakes_europe',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs)
        add_feature(
            category='physical', name='lakes_north_america',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs)


def add_ocean(edgecolor='#0978ab', facecolor='#c6ecff', linewidth=0.25,
              **kwargs):
    add_feature(
        category='physical', name='ocean',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)


def add_rivers(edgecolor='#0978ab', facecolor='none', linewidth=0.5,
               **kwargs):
    add_feature(
        category='physical', name='rivers_lake_centerlines',
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
    if 'scale' in kwargs and 'scale' == '10m':
        add_feature(
            category='physical', name='rivers_europe',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs)
        add_feature(
            category='physical', name='rivers_north_america',
            edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
            **kwargs)


def add_graticules(edgecolor='0.25', facecolor='none', linewidth=0.1,
                   interval=1, **kwargs):
    add_feature(
        category='physical', name='graticules_{}'.format(interval),
        edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth,
        **kwargs)
