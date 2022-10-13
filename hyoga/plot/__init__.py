# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga plotting tools to visualize glacier modelling datasets.
"""

from .colormaps import COLORMAPS, SEQUENCES
from .datasets import \
    bedrock_altitude, bedrock_altitude_contours, bedrock_erosion, \
    bedrock_hillshade, bedrock_isostasy, bedrock_shoreline, ice_margin, \
    surface_altitude_contours, surface_hillshade, surface_velocity, \
    surface_velocity_streamplot
from .hillshade import hillshade
from .naturalearth import feature, \
    cities, countries, country_borders, states, state_borders, \
    coastline, glaciers, graticules, lakes, ocean, rivers
from .shapefile import shapefile

__all__ = [
    'COLORMAPS', 'SEQUENCES',
    'bedrock_altitude', 'bedrock_altitude_contours', 'bedrock_erosion',
    'bedrock_hillshade', 'bedrock_isostasy', 'bedrock_shoreline', 'ice_margin',
    'surface_altitude_contours', 'surface_hillshade', 'surface_velocity',
    'surface_velocity_streamplot',
    'hillshade', 'feature',
    'cities', 'countries', 'country_borders', 'states', 'state_borders',
    'coastline', 'glaciers', 'graticules', 'lakes', 'ocean', 'rivers',
    'shapefile']
