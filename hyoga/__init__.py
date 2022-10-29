# Copyright (c) 2020-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""A thin wrapper around xarray to read and plot PISM output files."""

# module imports
from . import open

# object imports
from .core.accessor import HyogaDataset
from .core.config import config

__all__ = [
    'open',
    'config', 'HyogaDataset']
