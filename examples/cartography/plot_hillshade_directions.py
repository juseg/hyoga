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
    ds = ds.sel(x=slice(400e3, 435e3))

    # plot bedrock altitude
    for ax in axes:
        ds.hyoga.plot.bedrock_altitude(ax=ax, cmap='Topographic', vmin=0)

    # add hillshades
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[0], altitude=45, azimuth=315)
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[1], altitude=45, azimuth=[255, 315, 15],
        weight=[0.25, 0.5, 0.25])
    ds.hyoga.plot.bedrock_hillshade(
        ax=axes[2], altitude=45, azimuth=[15, 75, 135, 195, 255, 315],
        weight=[0.2, 0.125, 0.1, 0.125, 0.2, 0.25])

    # set titles
    axes[0].set_title('One direction')
    axes[1].set_title('Three directions (default)')
    axes[2].set_title('Six directions')

# show
plt.show()
