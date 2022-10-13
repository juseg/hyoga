# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a function to open global or regional paleoglacier extent
datasets. The data are returned as a geopandas GeoDataFrame instance, allowing
convenient postprocessing and speedy plotting.
"""

import os.path
import zipfile
import geopandas
import pandas
from hyoga.open.example import _download  # FIXME move to core?


def _download_paleoglaciers_ehl11():
    """Download Ehlers et al. (2011) paleoglaciers, return cache paths."""
    url = ('http://static.us.elsevierhealth.com/ehlers_digital_maps/'
           'digital_maps_02_all_other_files.zip')
    zipfilename = _download(url)
    cachedir = os.path.dirname(zipfilename)
    basenames = 'lgm', 'lgm_alpen'
    for basename in basenames:
        for ext in ('dbf', 'shp', 'shx'):
            filename = basename + '.' + ext
            if not os.path.isfile(os.path.join(cachedir, filename)):
                with zipfile.ZipFile(zipfilename, 'r') as archive:
                    archive.extract(filename, path=cachedir)
    return (os.path.join(cachedir, b+'.shp') for b in basenames)


def _download_paleoglaciers_bat19():
    """Download Batchelor et al. (2019) paleoglaciers, return cache path."""
    files = {'https://osf.io/gzkwc/download': 'LGM_best_estimate.dbf',
             'https://osf.io/xm6tu/download': 'LGM_best_estimate.prj',
             'https://osf.io/9bjwn/download': 'LGM_best_estimate.shx',
             'https://osf.io/9yhdv/download': 'LGM_best_estimate.shp'}
    for url, filename in files.items():
        filepath = _download(url, filename=filename)
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
        gdf = gdf.set_crs('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        gdf = gdf.drop_duplicates()

    # return geodataframe
    return gdf
