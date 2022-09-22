# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains functions to plot global or regional paleoglacier extent
datasets. These use hyoga's internal shapefile plotter which may increase speed
especially for high-definition data on small domains.
"""

import os.path
import zipfile
import hyoga.demo
import hyoga.plot


def _download_paleoglaciers_ehl11():
    """Download Ehlers et al. (2011) paleoglaciers, return cache paths."""
    url = ('http://static.us.elsevierhealth.com/ehlers_digital_maps/'
           'digital_maps_02_all_other_files.zip')
    zipfilename = hyoga.demo._download(url)  # FIXME W0212 protected-access
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
        filepath = hyoga.demo._download(url, filename=filename)
    return (filepath, )


def _download_paleoglaciers(source):
    """Download paleoglacier extent in cache dir."""
    return globals()['_download_paleoglaciers_' + source]()


def paleoglaciers(source='ehl11', **kwargs):
    """Plot Last Glacial Maximum paleoglacier extent.

    Parameters
    ----------
    source : 'ehl11' or 'bat19'
        Source of paleoglacier extent data, either Ehlers et al. (2011) or
        Batchelor et al. (2019).
    **kwargs : optional
        Keyword arguments passed to :func:`hyoga.plot.shapefile`.

    Returns
    -------
    geometries : tuple
        A tuple of :class:`cartopy.mpl.feature_artist.FeatureArtist`, or a
        nested tuple if a subject is passed to :func:`hyoga.plot.shapefile`.
    """
    # FIXME any way to combine ehl11 geometries to avoid returning a tuple?
    paths = _download_paleoglaciers(source)
    return tuple(hyoga.plot.shapefile(path, **kwargs) for path in paths)