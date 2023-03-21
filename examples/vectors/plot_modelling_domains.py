#!/usr/bin/env python
# Copyright (c) 2023, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Modelling domains
=================

Plot Ehlers et al. (2011) global paleoglacier data and default modelling
domains for the world and each continent.
"""

import matplotlib.pyplot as plt
import shapely
import geopandas
import hyoga.core.world


def plot_domain(ax, crs, name, properties):
    """Plot a single modelling from origin and bounds."""
    lat, lon, bounds = properties
    west, south, east, north = bounds
    vertices = [(west, south), (east, south), (east, north), (west, north)]
    polygon = shapely.geometry.Polygon(vertices)
    domain = geopandas.GeoSeries(polygon).set_crs(
        f'+proj=laea +lat_0={lat} +lon_0={lon} +ellps=WGS84')
    centroid = domain.centroid.to_crs(crs)
    domain.to_crs(crs).plot(ax=ax, ec='tab:red', fc='none')
    ax.annotate(
        name, xy=(centroid.x, centroid.y), xytext=(0, 12),
        textcoords='offset points', ha='center')


def plot_domains(ax, crs):
    """Plot modelling domains for the whole world."""
    world = hyoga.core.world.WORLD
    for name, properties in world.items():
        plot_domain(ax, crs, name, properties)


def plot_domains_map(crs='+proj=lonlat'):
    """Plot composite map with land, paleoglaciers, and modelling domains."""

    # plot map elements
    ax = hyoga.open.natural_earth('land').to_crs(crs).plot(color='0.9')
    hyoga.open.paleoglaciers('ehl11').to_crs(crs).plot(ax=ax, alpha=0.75)
    plot_domains(ax=ax, crs=crs)

    # set axes properties
    ax.set_title('Modelling domains')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)


# %%
# World
plot_domains_map()
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.show()

# %%
# North America
plot_domains_map(crs='+proj=laea +lat_0=55 +lon_0=-133 +ellps=WGS84 +units=m')
plt.xlim(-3000e3, 3000e3)
plt.ylim(-2000e3, 2000e3)
plt.show()
