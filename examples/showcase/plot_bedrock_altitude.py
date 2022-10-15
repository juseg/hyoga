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
import hyoga.open
import hyoga.plot

# initialize figure
ax = plt.subplot()

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(cmap='Topographic', vmin=0, vmax=4500)
    ds.hyoga.plot.bedrock_hillshade(ax=ax)

    # add coastline and rivers
    ds.hyoga.plot.naturalearth(ax=ax)

# set axes properties
ax.set_title('Bedrock altitude')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
