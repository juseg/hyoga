# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga plotting tools to visualize glacier modelling datasets.
"""

# FIXME following geopandas move this module will disappear

from .colormaps import COLORMAPS, SEQUENCES
from .hillshade import hillshade

__all__ = [
    'COLORMAPS', 'SEQUENCES',
    'hillshade']
