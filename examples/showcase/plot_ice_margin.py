#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ice margin
==========

Plot a composite map including bedrock altitude, an ice margin contour,
a half-transparent filled interior, and geographic elements.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import hyoga.open
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.dataset(hyoga.demo.get('pism.alps.out.2d.nc')) as ds:
    ds = ds.hyoga.where_thicker(1)

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, cmap='Greys', vmin=0, vmax=4500)
    ds.hyoga.plot.ice_margin(ax=ax, edgecolor='tab:blue', linewidths=1)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='tab:blue')

# add coastlines and rivers
ax.coastlines(edgecolor='0.25', linewidth=0.5)
ax.add_feature(
    cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale='10m'),
    edgecolor='0.25', facecolor='none', linewidth=0.5, zorder=0)

# set axes properties
ax.set_title('Ice margin')

# show
plt.show()
