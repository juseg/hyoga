#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
v0.2.0 Bale
===========
"""

import matplotlib.pyplot as plt
import contextily as cx
import hyoga

# plot paleoglaciers
ax = hyoga.open.paleoglaciers().to_crs(epsg=3857).plot(
    alpha=0.75, facecolor='w', edgecolor='r', linewidth=2)

# zoom on Bale Mountains (120x60 km)
ax.set_xlim(4390e3, 4470e3)
ax.set_ylim(730e3, 790e3)

# add stamen terrain
cx.add_basemap(ax, source=cx.providers.Stamen.TerrainBackground)

# set axes properties
ax.set_title('Bale Mountains')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
