#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock altitude contours
=========================

Plot a composite map including bedrock altitude contours, hillshade, and
geographic elements.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# get contours from colormap
cmap = plt.colormaps['Topographic']  # mpl >= 3.5

# open demo data
with xr.open_dataset(hyoga.demo.get('pism.alps.in.boot.nc')) as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude_contours(
        ax=ax, cmap='Topographic', vmin=0, vmax=4500)
    ds.hyoga.plot.bedrock_hillshade(ax=ax, zorder=1)

# add coastlines and rivers
ax.coastlines(edgecolor='0.25', linewidth=0.5)
ax.add_feature(
    cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale='10m'),
    edgecolor='0.25', facecolor='none', linewidth=0.5, zorder=0)

# set axes properties
ax.set_title('Bedrock altitude contours')

# show
plt.show()
