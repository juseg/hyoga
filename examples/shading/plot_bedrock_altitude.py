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
import hyoga

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(cmap='Topographic', vmin=0)
    ds.hyoga.plot.bedrock_hillshade()

    # add coastline and rivers
    ax = ds.hyoga.plot.natural_earth()

    # add scale bar
    ds.hyoga.plot.scale_bar()

# set title
ax.set_title('Bedrock altitude')

# show
plt.show()
