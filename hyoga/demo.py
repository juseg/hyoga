# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains utils to download demonstration data needed to plot
examples included in the documentation. There is currently only one function
but in the future more data may be dowloaded to demonstrate plotting time
series and plotting output from other models.
"""

import os.path
import urllib.parse
import warnings
import requests


def _download(url):
    """Download a file from the web, store in cache dir and return path."""
    cachedir = os.path.expanduser(os.path.join('~', '.cache', 'hyoga'))
    filepath = urllib.parse.urlparse(url).path
    filepath = os.path.basename(filepath)
    filepath = os.path.join(cachedir, filepath.split('/')[-1])
    if not os.path.isfile(filepath):
        os.makedirs(cachedir, exist_ok=True)
        with open(filepath, 'wb') as binaryfile:
            print("downloading {}...".format(url))
            binaryfile.write(requests.get(url).content)
    return filepath


def get(filename='pism.alps.out.2d.nc'):
    """Download a file from hyoga-data github repository."""
    repo = 'https://raw.githubusercontent.com/juseg/hyoga-data/main'
    model = filename.split('.')[0]
    url = '/'.join((repo, model, filename))
    return _download(url)


def pism_gridded():
    """Deprecated alias of get('pism.alps.out.2d.nc')."""
    warnings.warn(
        "pism_gridded() is deprecated and will be removed in v0.3.0, use "
        "get('pism.alps.out.2d.nc') instead", FutureWarning)
    return get('pism.alps.out.2d.nc')


def pism_series():
    """Deprecated alias of get('pism.alps.out.1d.nc')."""
    warnings.warn(
        "pism_gridded() is deprecated and will be removed in v0.3.0, use "
        "get('pism.alps.out.1d.nc') instead", FutureWarning)
    return get('pism.alps.out.1d.nc')
