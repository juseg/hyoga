#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock isostasy
================

Plot a composite map including bedrock altitude, surface altitude contours,
bedroc isostatic adjustment relative to a reference topography in a separate
model input file, and geographic elements.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with xr.open_dataset(hyoga.demo.get('pism.alps.out.2d.nc')) as ds:

    # compute isostasy using separate boot file
    ds = ds.hyoga.assign_isostasy(hyoga.demo.get('pism.alps.in.boot.nc'))

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.bedrock_isostasy(
        ax=ax, cbar_ax=cax, levels=[-150, -100, -50, 0, 0.5, 1, 1.5])
    ds.hyoga.plot.ice_margin(ax=ax)

# add coastlines and rivers
ax.coastlines(edgecolor='0.25', linewidth=0.5)
ax.add_feature(
    cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale='10m'),
    edgecolor='0.25', facecolor='none', linewidth=0.5, zorder=0)

# set axes properties
cax.set_ylabel('')
ax.set_title('Bedrock isostatic adjustment (m)')

# show
plt.show()
