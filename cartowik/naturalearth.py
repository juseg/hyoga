# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
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

def _add_subject_feature(category=None, name=None, scale=None, **kwargs):
    """Plot Natural Earth feature iallowing a different color for the
    subject."""
    fname = cshp.natural_earth(resolution=scale, category=category, name=name)
    _add_subject_shpfile(fname, **kwargs)


def _add_subject_shpfile(filename, ax=None, facecolor=None, subject=None,
                         subject_facecolor=None, **kwargs):
    """Plot shapefile geometries allowing a different color for the subject."""

    # get current axes if None provided
    ax = ax or plt.gca()

    # prepare axes extent geometry
    crs = ccrs.PlateCarree()
    axes_box = _get_extent_geometry(ax=ax, crs=crs)

    # open shapefile data
    shp = cshp.Reader(filename)

    # loop on records
    for rec in shp.records():
        attr = 'name' if 'name' in rec.attributes else 'NAME'
        if subject is not None and rec.attributes[attr] == subject:
            color = subject_facecolor
        else:
            color = facecolor

        # add intersecting geometries
        if rec.geometry is not None and axes_box.intersects(rec.geometry):
            ax.add_geometries(rec.geometry, crs, facecolor=color, **kwargs)


def _get_extent_geometry(ax=None, crs=None):
    """Return axes extent as shapely geometry."""
    ax = ax or plt.gca()
    west, east, south, north = ax.get_extent(crs=crs)
    return sgeom.box(west, south, east, north)


# Natural Earth cultural
# ----------------------

def add_countries(ax=None, facecolor='#e0e0e0', scale='10m',
                  subject=None, subject_facecolor='#fefee9'):
    _add_subject_feature(
        ax=ax, category='cultural', name='admin_0_countries', scale=scale,
        subject=subject, subject_facecolor=subject_facecolor,
        facecolor=facecolor)


def add_country_borders(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='cultural', name='admin_0_boundary_lines_land',
        scale=scale, edgecolor='#646464', facecolor='none', linewidth=2.0)
    _add_subject_feature(
        ax=ax, category='cultural', name='admin_0_boundary_lines_map_units',
        scale=scale, edgecolor='#646464', facecolor='none', linewidth=1.5)


def add_states(ax=None, facecolor='#e0e0e0', scale='10m',
               subject=None, subject_facecolor='#fefee9'):
    _add_subject_feature(
        ax=ax, category='cultural', name='admin_1_states_provinces',
        scale=scale, subject=subject, subject_facecolor=subject_facecolor,
        facecolor=facecolor)


def add_state_borders(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='cultural', name='admin_1_states_provinces_lines',
        scale=scale, edgecolor='#646464', facecolor='none', linewidth=1.0)


# Natural Earth physical
# ----------------------

def add_coastline(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='physical', name='coastline', scale=scale,
        edgecolor='#0978ab', facecolor='none', lw=0.25)


def add_lakes(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='physical', name='lakes', scale=scale,
        edgecolor='#0978ab', facecolor='#d8f2fe', lw=0.25)
    _add_subject_feature(
        ax=ax, category='physical', name='lakes_europe', scale=scale,
        edgecolor='#0978ab', facecolor='#d8f2fe', lw=0.25)
    _add_subject_feature(
        ax=ax, category='physical', name='lakes_north_america', scale=scale,
        edgecolor='#0978ab', facecolor='#d8f2fe', lw=0.25)


def add_ocean(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='physical', name='ocean', scale=scale,
        edgecolor='#0978ab', facecolor='#c6ecff', lw=0.25)


def add_rivers(ax=None, scale='10m'):
    _add_subject_feature(
        ax=ax, category='physical', name='rivers_lake_centerlines',
        scale=scale, edgecolor='#0978ab', facecolor='none', lw=0.5)
    _add_subject_feature(
        ax=ax, category='physical', name='rivers_europe', scale=scale,
        edgecolor='#0978ab', facecolor='none', lw=0.5)
    _add_subject_feature(
        ax=ax, category='physical', name='rivers_north_america', scale=scale,
        edgecolor='#0978ab', facecolor='none', lw=0.5)
