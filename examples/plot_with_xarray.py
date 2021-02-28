#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot surface velocity
=====================

Plot Alps dataset surface velocity map.
"""

import matplotlib.pyplot as plt
import hyoga.open
import hyoga.demo

# initialize figure
ax = plt.axes()

# open demo data
with hyoga.open.dataset(hyoga.demo.gridded()) as ds:
    ds = ds.sel(age=24)
    ds = ds.hyoga.where_thicker(1)

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.surface_velocity(ax=ax, vmin=1e1, vmax=1e3)
    ds.hyoga.plot.ice_margin(ax=ax)

    # needed to avoid distorsion
    ax.set_aspect('equal')

plt.show()
