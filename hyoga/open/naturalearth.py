# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a function to open globally-available Natural Earth data,
including cultural (cities, countries, etc) and physical (lakes, rivers,
glaciers, etc) elements. The data are returned as a geopandas GeoDataFrame
instance, allowing convenient postprocessing and speedy plotting.
"""

import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as cshp
import geopandas
import hyoga.plot
import matplotlib.pyplot as plt


def naturalearth(category=None, name=None, scale='10m'):
    """Open Natural Earth geodataframe

    Parameters
    ----------
    category : {'cultural', 'physical'}, optional
        Natural Earth data category (i.e. folder) used for downloads.
    name : str, optional
        Natural Earth feature name, such as ``lakes`` or ``admin_0_countries``
        (used to determine the name of the shapefile to download). Please
        browse https://www.naturalearthdata.com to see what data is available.
    scale : {'10m', '50m', '110m'}, optional
        Natural Earth data scale controlling the level of detail (and plotting
        speed). Unlike cartopy this defaults to the largest scale of '10m'.

    Returns
    -------
    gdf : GeoDataFrame
        The geodataframe containing Natural Earth geometries.
    """
    # TODO in 0.2.0: replace functions below with alias kwarg
    # TODO in 0.2.x: replace cartopy.io with internal downloader
    return geopandas.read_file(cartopy.io.shapereader.natural_earth(
        category=category, name=name, resolution=scale))


def feature(category=None, name=None, scale='10m', crs=None, zorder=-1, **kwargs):
    """Plot Natural Earth feature allowing a different color for subject.

    Parameters
    ----------
    category : {'cultural', 'physical'}, optional
        Natural Earth data category (i.e. folder) used for downloads.
    name : str, optional
        Natural Earth feature name, such as ``lakes`` or ``admin_0_countries``
        (used to determine the name of the shapefile to download). Please
        browse https://www.naturalearthdata.com to see what data is available.
    scale : {'10m', '50m', '110m'}, optional
        Natural Earth data scale controlling the level of detail (and plotting
        speed). Unlike cartopy this defaults to the largest scale of '10m'.
    crs : str or pyproj.CRS, optional
        Cartographic reference system to reproject feature to before plotting.
        Can be anything supported by :meth:`geopandas.GeoDataFrame.to_crs`
        such as a proj4 string, "epsg:4326", or a WKT string.
    zorder : float, optional
        Set the matplotlib zorder attribute of the resulting feature artist(s).
        Artists with lower zorder values are drawn first. The default value of
        -1 ensures that Natural Earth data are drawn early as a background to
        other plot elements.
    **kwargs :
        Additional keyword arguments are passed to
        :func:`geopandas.GeoDataFrame.plot`.

    Returns
    -------
    ax : :class:`matplotlib.axes.Axes` (or a subclass)
        Matplotlib axes used for plotting.
    """
    # open Natural Earth shapefile
    gdf = naturalearth(category=category, name=name, scale=scale)

    # reproject if crs is not None
    if crs is not None:
        gdf = gdf.to_crs(crs=crs)

    # plot and return axes
    return gdf.plot(zorder=zorder, **kwargs)


# Natural Earth cultural
# ----------------------

def cities(ax=None, lang=None, include=None, exclude=None, ranks=None,
           **kwargs):
    """Plot populated places as an annotated scatter plot.

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


def countries(**kwargs):
    # IDEA: style='wiki' => facecolor='#e0e0e0', subject_facecolor='#fefee9'
    style = dict(edgecolor='none', facecolor='0.9', linewidth=1)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(
        category='cultural', name='admin_0_countries', **style)


def country_borders(**kwargs):
    # IDEA: style='wiki' => linestyle=(0, (5, 2.5, 1.25, 2.5))
    style = dict(edgecolor='0.4', facecolor='none', linewidth=2.5)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return (
        feature(
            category='cultural', name='admin_0_boundary_lines_land',
            **style),
        feature(
            category='cultural', name='admin_0_boundary_lines_map_units',
            **style))


def states(**kwargs):
    style = dict(edgecolor='none', facecolor='0.9', linewidth=0.25)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(
        category='cultural', name='admin_1_states_provinces',
        **style)


def state_borders(**kwargs):
    style = dict(edgecolor='0.4', facecolor='none', linewidth=1)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    # IDEA: style='wiki' => edgecolor='#646464'
    return feature(
        category='cultural', name='admin_1_states_provinces_lines', **style)


# Natural Earth physical
# ----------------------

def coastline(**kwargs):
    style = dict(edgecolor='0.25', facecolor='none', linewidth=0.25)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(
        category='physical', name='coastline', **style)


def glaciers(**kwargs):
    style = dict(edgecolor='0.25', facecolor='1.0', linewidth=0.25)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(
        category='physical', name='glaciated_areas', **style)


def lakes(**kwargs):
    style = dict(edgecolor='0.25', facecolor='0.95', linewidth=0.25)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    # IDEA: style='wiki' => edgecolor='#0978ab', facecolor='#d8f2fe'
    kwargs = dict(category='physical', **style)
    features = feature(name='lakes', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    feature(name='lakes_europe', **kwargs),
                    feature(name='lakes_north_america', **kwargs))
    return features


def ocean(**kwargs):
    style = dict(edgecolor='0.25', facecolor='0.95', linewidth=0.25)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(category='physical', name='ocean', **style)


def rivers(**kwargs):
    style = dict(edgecolor='0.25', facecolor='none', linewidth=0.5)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    kwargs = dict(category='physical', **style)
    features = feature(name='rivers_lake_centerlines', **kwargs)
    if 'scale' not in kwargs or kwargs['scale'] == '10m':
        features = (features,
                    feature(name='rivers_europe', **kwargs),
                    feature(name='rivers_north_america', **kwargs))
    return features


def graticules(interval=1, **kwargs):
    style = dict(edgecolor='0.25', facecolor='none', linewidth=0.1)
    style.update(**kwargs)  # in Py 3.9 kwargs = defaults | kwargs
    return feature(
        category='physical', name='graticules_{}'.format(interval), **style)
