# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a function to open globally-available Natural Earth data,
including cultural (cities, countries, etc) and physical (lakes, rivers,
glaciers, etc) elements. The data are returned as a geopandas GeoDataFrame
instance, allowing convenient postprocessing and speedy plotting.
"""

import geopandas
import pandas
import hyoga.plot


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
    downloader = hyoga.open.downloader.NaturalEarthDownloader()
    filepath = downloader(scale, category, theme)
    return geopandas.read_file(filepath)
