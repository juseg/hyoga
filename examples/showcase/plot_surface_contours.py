#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Surface contours
================

Plot a composite map including bedrock altitude, a half-transparent ice mask,
a surface altitude contour, and geographic elements.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=3000)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='w')
    ds.hyoga.plot.surface_altitude_contours(ax=ax, colors='tab:blue')

# add coastlines and rivers
hyoga.plot.coastline(ax=ax)
hyoga.plot.rivers(ax=ax)
hyoga.plot.lakes(ax=ax)

# set axes properties
ax.set_title(r'Surface elevation contours')

# show
plt.show()
