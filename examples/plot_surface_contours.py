#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot surface contours
=====================
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import hyoga.open
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.dataset(hyoga.demo.pism_gridded()) as ds:
    ds = ds.sel(age=24)
    ds = ds.hyoga.where_thicker(1)

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=3000)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='w')
    ds.hyoga.plot.surface_altitude_contours(ax=ax)

# add coastlines and rivers
ax.coastlines(edgecolor='0.25', linewidth=0.5)
ax.add_feature(
    cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale='10m'),
    edgecolor='0.25', facecolor='none', linewidth=0.5, zorder=0)

# show
plt.show()
