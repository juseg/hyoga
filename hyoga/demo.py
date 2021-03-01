# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains utils to download demonstration data needed to plot
examples included in the documentation. There is currently only one function
but in the future more data may be dowloaded to demonstrate plotting time
series and plotting output from other models.
"""

import os.path
import requests


def _download(url):
    """Download a file from the web, store in cache dir and return path."""
    cachedir = os.path.expanduser(os.path.join('~', '.cache', 'hyoga'))
    filename = os.path.join(cachedir, url.split('/')[-1])
    if not os.path.isfile(filename):
        os.makedirs(cachedir, exist_ok=True)
        with open(filename, 'wb') as binaryfile:
            print("downloading {}...".format(url))
            binaryfile.write(requests.get(url).content)
    return filename


def _download_zenodo(record, filename):
    """Download a file from Zenodo based on record number and filename."""
    url = 'https://zenodo.org/record/{}/files/{}'.format(record, filename)
    return _download(url)


def pism_gridded():
    """Download Alps public gridded data from Zenodo, return path."""
    return _download_zenodo(
        record='3604142', filename='alpcyc.1km.epic.pp.ex.1ka.nc')


def pism_series():
    """Download Alps public gridded data from Zenodo, return path."""
    return _download_zenodo(
        record='3604142', filename='alpcyc.1km.epic.pp.ts.10a.nc')
