#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Interpolated output
===================

Demonstrate interpolating two-dimensional model output onto a higher-resolution
topography provided in a separate file. Bedrock isostatic adjustment needs to
be informed in order to correct for the offset between the model and the
high-resolution bedrock topographies. This is a rather extreme example with a
ten-fold increase in horizontal resolution.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.example('pism.alps.out.2d.nc') as ds:

    # compute isostatic adjustment from a reference input topography
    ds = ds.hyoga.assign_isostasy(hyoga.open.example('pism.alps.in.boot.nc'))

    # perform the actual interpolation
    ds = ds.hyoga.interp(hyoga.open.example('pism.alps.vis.refined.nc'))

    # plot model output
    ds.hyoga.plot.bedrock_altitude(
        ax=ax, cmap='gist_earth', vmin=-3000, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='w')

# set axes properties
ax.set_title('Interpolated output')

# show
plt.show()
