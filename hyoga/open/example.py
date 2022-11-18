# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide a function to download sample data needed to plot examples
included in the documentation. There are currently only few files available
but in the future more data may be dowloaded to demonstrate plotting time
series and plotting output from other models.
"""

import xarray as xr

import hyoga.open.downloader


def example(filename='pism.alps.out.2d.nc'):
    """Open cached example dataset from hyoga-data github repository."""
    repo = 'https://raw.githubusercontent.com/juseg/hyoga-data/main'
    model = filename.split('.')[0]
    url = '/'.join((repo, model, filename))
    path = hyoga.open.downloader.CacheDownloader()(url, filename)
    return xr.open_dataset(path)
