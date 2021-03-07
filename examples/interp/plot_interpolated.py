#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot interpolated output
========================
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import hyoga.open
import hyoga.demo

# initialize figure
ax = plt.subplot(projection=ccrs.UTM(32))

# open demo data
with hyoga.open.dataset(hyoga.demo.get('pism.alps.out.2d.nc')) as ds:
    ds = ds.hyoga.assign_isostasy(hyoga.demo.get('pism.alps.in.boot.nc'))
    ds = ds.hyoga.interp(hyoga.demo.get('pism.alps.vis.refined.nc'))

    # plot model output
    ds.hyoga.plot.bedrock_altitude(ax=ax, cmap='YlOrBr', vmin=0, vmax=4500)
    ds.hyoga.plot.surface_altitude_contours(ax=ax)
    ds.hyoga.plot.ice_margin(ax=ax, facecolor='w')

# set axes properties
ax.set_title('Interpolated output')

# show
plt.show()
