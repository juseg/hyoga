# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga input tools to open glacier modelling datasets.
"""

from .example import example
from .local import dataset, mfdataset, subdataset
from .naturalearth import natural_earth
from .paleoglaciers import paleoglaciers

__all__ = [
    'example',
    'dataset', 'mfdataset', 'subdataset',
    'natural_earth',
    'paleoglaciers']
