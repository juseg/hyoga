#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock altitude
================

Plot a composite map including bedrock altitude, hillshade, and geographic
elements.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import hyoga.open
import hyoga.plot

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(cmap='Topographic', vmin=0, vmax=4500)
    ds.hyoga.plot.bedrock_hillshade(ax=ax)

# add coastlines and rivers
hyoga.plot.coastline(ax=ax)
hyoga.plot.rivers(ax=ax)
hyoga.plot.lakes(ax=ax)

# set axes properties
ax.set_title('Bedrock altitude')

# show
plt.show()
