# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a function to open global or regional paleoglacier extent
datasets. The data are returned as a geopandas GeoDataFrame instance, allowing
convenient postprocessing and speedy plotting.
"""

import geopandas
import pandas

import hyoga.open.downloader


def _download_paleoglaciers_ehl11():
    """Download Ehlers et al. (2011) paleoglaciers, return cache paths."""
    # FIXME store shapefiles in subdirectory
    url = ('http://static.us.elsevierhealth.com/ehlers_digital_maps/'
           'digital_maps_02_all_other_files.zip')
    downloader = hyoga.open.downloader.ShapeZipDownloader()
    return (
        downloader(url, path) for path in ('lgm.shp', 'lgm_alpen.shp'))


def _download_paleoglaciers_bat19():
    """Download Batchelor et al. (2019) paleoglaciers, return cache path."""
    downloader = hyoga.open.downloader.OSFDownloader()
    downloader('gzkwc', 'LGM_best_estimate.dbf')
    downloader('xm6tu', 'LGM_best_estimate.prj')
    downloader('9bjwn', 'LGM_best_estimate.shx')
    filepath = downloader('9yhdv', 'LGM_best_estimate.shp')
    return (filepath, )


def _download_paleoglaciers(source):
    """Download paleoglacier extent in cache dir."""
    return globals()['_download_paleoglaciers_' + source]()


def paleoglaciers(source='ehl11'):
    """Open Last Glacial Maximum paleoglacier extent.

    Parameters
    ----------
    source : 'ehl11' or 'bat19'
        Source of paleoglacier extent data, either Ehlers et al. (2011) or
        Batchelor et al. (2019).

    Returns
    -------
    gdf : GeoDataFrame
        The geodataframe containing paleoglaciers geometries.
    """
    # open paleoglacier shapefile(s)
    paths = _download_paleoglaciers(source)
    gdf = pandas.concat(geopandas.read_file(path) for path in paths)

    # Ehlers et al. data need cleanup
    # FIXME move to _paleoglaciers_ehl11
    if source == 'ehl11':
        gdf = gdf.drop_duplicates()

    # return geodataframe
    return gdf
