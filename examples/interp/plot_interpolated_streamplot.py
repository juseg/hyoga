#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Interpolated streamplot
=======================

Demonstrate combining two-dimensional model output spatial interpolation with a
surface velocity streamplot. The streamplot method does an interpolation on its
own, and consumes a lot of memory when applied on large arrays. Therefore it is
advisable to run it on the original rather than the interpolated data.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))
cax = plt.axes([0.15, 0.55, 0.025, 0.25])

# open demo data
with xr.open_dataset(hyoga.demo.get('pism.alps.out.2d.nc')) as ds:
    ds = ds.hyoga.assign_isostasy(hyoga.demo.get('pism.alps.in.boot.nc'))
    interp = ds.hyoga.interp(hyoga.demo.get('pism.alps.vis.refined.nc'))

    # plot model output
    interp.hyoga.plot.bedrock_altitude(
        ax=ax, cmap='gist_earth', vmin=-3000, vmax=4500)
    interp.hyoga.plot.surface_altitude_contours(ax=ax)
    interp.hyoga.plot.ice_margin(ax=ax, facecolor='w')

    # plot streamplot from non-interpolated data
    streams = ds.hyoga.plot.surface_velocity_streamplot(
        ax=ax, cmap='Blues', vmin=1e1, vmax=1e3, density=(6, 4))

    # add colorbar manually
    ax.figure.colorbar(streams.lines, cax=cax, extend='both')

# set axes properties
ax.set_title(r'Interpolated output (m$\,$a$^{-1}$)')

# show
plt.show()
