#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ice margin
==========

Plot a composite map including bedrock altitude, an ice margin contour,
a half-transparent filled interior, and geographic elements.
"""

import matplotlib.pyplot as plt
import hyoga

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(cmap='Greys', vmin=0, vmax=4500)
    ds.hyoga.plot.ice_margin(edgecolor='tab:blue', linewidths=1)
    ds.hyoga.plot.ice_margin(facecolor='tab:blue')

    # add coastline and rivers
    ax = ds.hyoga.plot.natural_earth()

# set axes properties
ax.set_title('Ice margin')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
