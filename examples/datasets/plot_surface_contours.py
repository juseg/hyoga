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
import hyoga

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=3000)
    ds.hyoga.plot.ice_margin(facecolor='w')
    ds.hyoga.plot.surface_altitude_contours(colors='tab:blue')

    # add coastline and rivers
    ax = ds.hyoga.plot.natural_earth()

# set axes properties
ax.set_title(r'Surface elevation contours')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
