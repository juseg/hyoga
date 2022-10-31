#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock isostasy
================

Plot a composite map including bedrock altitude, surface altitude contours,
bedroc isostatic adjustment relative to a reference topography in a separate
model input file, and geographic elements.
"""

import matplotlib.pyplot as plt
import hyoga

# initialize figure
ax = plt.subplot()
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # compute isostasy using separate boot file
    ds = ds.hyoga.assign_isostasy(hyoga.open.example('pism.alps.in.boot.nc'))

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.bedrock_isostasy(
        ax=ax, cbar_ax=cax, levels=[-150, -100, -50, 0, 0.5, 1, 1.5])
    ds.hyoga.plot.ice_margin(ax=ax)

    # add coastline and rivers
    ds.hyoga.plot.natural_earth(ax=ax)

# set axes properties
cax.set_ylabel('')
ax.set_title('Bedrock isostatic adjustment (m)')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
