# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module is deprecated and will be removed in v0.4.0, use ``open.example``
instead.
"""

import warnings
from hyoga.open.example import _download_example


def get(filename='pism.alps.out.2d.nc'):
    """Deprecated function to download demo file and return path."""
    warnings.warn(
        "demo.get() -> url is deprecated and will be removed in v0.4.0, use "
        "open.example() -> dataset instead", FutureWarning)
    return _download_example(filename)


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
