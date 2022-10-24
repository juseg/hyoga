#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Interpolated streamplot
=======================

Demonstrate combining two-dimensional model output spatial interpolation with a
surface velocity streamplot. The streamplot method does an interpolation on its
own. When applied to larger domains it may be advisable to run it on the
original rather than interpolated data.
"""

import matplotlib.pyplot as plt
import hyoga

# initialize figure
ax = plt.subplot()
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:
    ds = ds.hyoga.assign_isostasy(hyoga.open.example('pism.alps.in.boot.nc'))
    ds = ds.hyoga.interp(hyoga.open.example('pism.alps.vis.refined.nc'))

    # plot model output
    ds.hyoga.plot.bedrock_altitude(
        ax=ax, cmap='gist_earth', vmin=-3000, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='w')

    # plot streamplot
    streams = ds.hyoga.plot.surface_velocity_streamplot(
        ax=ax, cmap='Blues', vmin=1e1, vmax=1e3, density=(6, 4))

    # add colorbar manually
    ax.figure.colorbar(streams.lines, cax=cax, extend='both')

# set axes properties
ax.set_title(r'Interpolated output (m$\,$a$^{-1}$)')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_aspect('equal')

# show
plt.show()
