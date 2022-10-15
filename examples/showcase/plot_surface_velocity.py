#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Surface velocity
================

Plot a composite map including bedrock altitude, surface topography contours,
a surface velocity map, and geographic elements.
"""

import matplotlib.pyplot as plt
import hyoga.open
import hyoga.plot

# initialize figure
ax = plt.subplot()
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.surface_velocity(ax=ax, cbar_ax=cax, vmin=1e1, vmax=1e3)
    ds.hyoga.plot.ice_margin(ax=ax)

    # add coastline and rivers
    ds.hyoga.plot.naturalearth(ax=ax)

# set axes properties
cax.set_ylabel('')
ax.set_title(r'Surface velocity (m$\,$a$^{-1}$)')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
