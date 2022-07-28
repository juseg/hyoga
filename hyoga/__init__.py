# Copyright (c) 2020-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""A thin wrapper around xarray to read and plot PISM output files."""

# Only import HyogaDataset here. This registers the accessor. In practice this
# also triggers importing open (in the future this will change) and plot.

from .conf import config
from .hyoga import HyogaDataset

__all__ = ['config', 'HyogaDataset']
