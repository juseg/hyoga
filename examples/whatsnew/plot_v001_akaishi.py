#!/usr/bin/env python
# Copyright (c) 2021-2024, Julien Seguinot (juseg.dev)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
v0.1.0 Akaishi
==============
"""

import matplotlib.pyplot as plt
import contextily as cx
import hyoga

# plot paleoglaciers
ax = hyoga.open.paleoglaciers().to_crs(epsg=3857).plot(
    alpha=0.75, facecolor='tab:blue', edgecolor='tab:blue', linewidth=2)

# zoom on Akaishi Mountains
ax.set_xlim(15330e3, 15450e3)
ax.set_ylim(4200e3, 4290e3)

# add stamen terrain
cx.add_basemap(ax, source=cx.providers.Esri.WorldShadedRelief)

# set axes properties
ax.set_title('Akaishi Mountains')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# show
plt.show()
