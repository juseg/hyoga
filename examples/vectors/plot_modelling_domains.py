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
    domain_crs = f'+proj=laea +lat_0={lat} +lon_0={lon} +ellps=WGS84'
    domain = geopandas.GeoSeries(polygon).set_crs(domain_crs)
    domain.to_crs(crs).plot(ax=ax, ec='tab:red', fc='none')


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
plot_domains_map(crs='+proj=laea +lat_0=54 +lon_0=-133 +ellps=WGS84')
plt.title('Modelling domains (North America)')
plt.xlim(-3000e3, 3000e3)
plt.ylim(-2000e3, 2000e3)
plt.show()

# %%
# South America
plot_domains_map(crs='+proj=laea +lat_0=-24 +lon_0=-58 +ellps=WGS84')
plt.title('Modelling domains (South America)')
plt.xlim(-6000e3, 6000e3)
plt.ylim(-4500e3, 4500e3)
plt.show()

# %%
# Europe
plot_domains_map(crs='+proj=laea +lat_0=56 +lon_0=21 +ellps=WGS84')
plt.title('Modelling domains (Europe)')
plt.xlim(-3000e3, 3000e3)
plt.ylim(-2000e3, 2000e3)
plt.show()

# %%
# Africa
plot_domains_map(crs='+proj=laea +lat_0=3 +lon_0=35 +ellps=WGS84')
plt.title('Modelling domains (Africa)')
plt.xlim(-3000e3, 3000e3)
plt.ylim(-2000e3, 2000e3)
plt.show()

# %%
# Asia
plot_domains_map(crs='+proj=laea +lat_0=55 +lon_0=105 +ellps=WGS84')
plt.title('Modelling domains (Asia)')
plt.xlim(-4500e3, 4500e3)
plt.ylim(-3000e3, 3000e3)
plt.show()

# %%
# Oceania
plot_domains_map(crs='+proj=laea +lat_0=-43 +lon_0=158 +ellps=WGS84')
plt.title('Modelling domains (Oceania)')
plt.xlim(-3000e3, 3000e3)
plt.ylim(-2000e3, 2000e3)
plt.show()
