#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock erosion
===============

Plot a composite map including bedrock altitude, surface altitude contours,
bedrock erosion computed from basal ice velocity, and geographic elements.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker
import cartopy.crs as ccrs
import hyoga.open
import hyoga.plot

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.bedrock_erosion(
        ax=ax, cbar_ax=cax, levels=[10**i for i in range(-9, 1)],
        cbar_kwargs=dict(
            format=matplotlib.ticker.LogFormatterMathtext(),
            ticks=[10**i for i in range(-9, 1, 3)]))
    ds.hyoga.plot.ice_margin(ax=ax)

# add coastlines and rivers
hyoga.plot.coastline(ax=ax)
hyoga.plot.rivers(ax=ax)
hyoga.plot.lakes(ax=ax)

# set axes properties
cax.set_ylabel('')
ax.set_title(r'Glacier erosion rate (mm$\,$a$^{-1}$)')

# show
plt.show()
