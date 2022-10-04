#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Multidirectional hillshade
==========================

Plot shaded relief map using a single and multiple illumination angles.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import hyoga.open

# initialize figure
fig, axes = plt.subplots(ncols=3, subplot_kw=dict(projection=ccrs.UTM(32)))

# open demo data with refined topography
with hyoga.open.example('pism.alps.vis.refined.nc') as ds:
    ds = ds.sel(x=slice(402e3, 427e3))

    # plot bedrock altitude
    for ax in axes:
        ds.hyoga.plot.bedrock_altitude(ax=ax, cmap='Topographic', vmin=0)

    # add hillshades
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[0], altitude=30, azimuth=330)
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[1], altitude=[60, 0, 60], azimuth=[260, 330, 30])
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[2], altitude=[60, 30, 0, 30, 60],
        azimuth=[210, 260, 330, 30, 90])

    # set titles
    axes[0].set_title('One direction')
    axes[1].set_title('Three directions')
    axes[2].set_title('Five directions')

# show
plt.show()
