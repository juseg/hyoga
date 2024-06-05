#!/usr/bin/env python
# Copyright (c) 2023-2024, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
v0.3.0 Cantal
=============
"""

import matplotlib.pyplot as plt
import contextily as cx
import hyoga

# plot paleoglaciers
ax = hyoga.open.paleoglaciers().to_crs(epsg=3857).plot(
    alpha=0.75, facecolor='tab:blue', edgecolor='tab:blue', linewidth=2)

# zoom on Cocuy (240x180 km)
ax.set_xlim(-8200e3, -7960e3)
ax.set_ylim(580e3, 760e3)

# add stamen terrain
cx.add_basemap(ax, source=cx.providers.Esri.WorldShadedRelief)

# set axes properties
ax.set_title('Cocuy')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
