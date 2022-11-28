#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Bedrock altitude contours
=========================

Plot a composite map including bedrock altitude contours, hillshade, and
geographic elements. In absence of a ``levels`` argument, the altitude levels
are internally optimized to fit the ``Topographic`` colormap.
"""

import matplotlib.pyplot as plt
import hyoga

# initialize figure
ax = plt.subplot()
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude_contours(
        ax=ax, cbar_ax=cax, cmap='Topographic', vmin=0, vmax=4500)
    ds.hyoga.plot.bedrock_hillshade(ax=ax)

    # add coastline and rivers
    ds.hyoga.plot.natural_earth(ax=ax)

# set axes properties
ax.set_title('Bedrock altitude contours')
cax.set_ylabel('')

# show
plt.show()
