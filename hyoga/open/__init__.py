# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga input tools to open glacier modelling datasets.
"""

from .local import dataset, mfdataset, subdataset

__all__ = [
    'dataset', 'mfdataset', 'subdataset']
