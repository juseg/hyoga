# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga plotting tools to visualize glacier modelling datasets.
"""

from .colormaps import COLORMAPS, SEQUENCES
from .hillshade import hillshade
from .naturalearth import feature, \
    cities, countries, country_borders, states, state_borders, \
    coastline, glaciers, graticules, lakes, ocean, rivers
from .paleoglaciers import paleoglaciers
from .shapefile import shapefile

__all__ = [
    'COLORMAPS', 'SEQUENCES', 'hillshade', 'feature',
    'cities', 'countries', 'country_borders', 'states', 'state_borders',
    'coastline', 'glaciers', 'graticules', 'lakes', 'ocean', 'rivers',
    'paleoglaciers', 'shapefile']
