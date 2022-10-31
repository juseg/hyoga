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
import pandas
import hyoga.plot
import matplotlib.pyplot as plt


def natural_earth(theme, category='physical', scale='10m'):
    """Open Natural Earth geodataframe

    Parameters
    ----------
    theme : str or iterable
        Natural Earth data theme(s), such as ``lakes`` or ``admin_0_countries``
        (used to determine the name(s) of the shapefile(s) to download), or one
        of the ``lakes_all`` and ``rivers_all`` aliases to open respecively all
        lakes and rivers including regional subsets (at 10m scale). Please
        browse https://www.naturalearthdata.com for available themes.
    category : {'cultural', 'physical'}, optional
        Natural Earth data category (i.e. online folder) used for downloads,
        defaults to 'physical'.
    scale : {'10m', '50m', '110m'}, optional
        Natural Earth data scale controlling the level of detail, defaults to
        the highest scale of 10m.

    Returns
    -------
    gdf : GeoDataFrame
        The geodataframe containing Natural Earth geometries.
    """

    # process theme aliases
    aliases = {
        'lakes_all': (
            'lakes', 'lakes_australia', 'lakes_europe', 'lakes_north_america'),
        'rivers_all': (
            'rivers_lake_centerlines', 'rivers_australia', 'rivers_europe',
            'rivers_north_america')}
    if isinstance(theme, str) and theme in aliases:
        theme = aliases[theme]

    # if theme is iterable, call recursively
    if hasattr(theme, '__iter__') and not isinstance(theme, str):
        return pandas.concat(natural_earth(
            subtheme, category=category, scale=scale) for subtheme in theme)

    # otherwise, return geodataframe
    # TODO in 0.2.x: replace cartopy.io with internal downloader
    return geopandas.read_file(cartopy.io.shapereader.natural_earth(
        category=category, name=theme, resolution=scale))


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
