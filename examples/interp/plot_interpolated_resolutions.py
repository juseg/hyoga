#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Grid refinement
===============

Demonstrate two-dimensional model output interpolation onto grids with
increasing spatial resolution. The leftmost panel shows the original data with
a spatial resolution of 1 km, and other panels show interpolated results.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import hyoga.demo

# initialize figure
fig, axes = plt.subplots(ncols=4, subplot_kw=dict(projection=ccrs.UTM(32)))
resolutions = [500, 200, 100]

# open 100m resolution topography for edits
with xr.open_dataset(hyoga.demo.get('pism.alps.vis.refined.nc')) as ds:
    topo = ds.hyoga.getvar('bedrock_altitude')
    topo = topo.sel(x=slice(402e3, 427e3))

# open demo data
with xr.open_dataset(hyoga.demo.get('pism.alps.out.2d.nc')) as ds:
    ds = ds.hyoga.assign_isostasy(hyoga.demo.get('pism.alps.in.boot.nc'))

    # plot original data
    ax = axes[0]
    masked = ds.hyoga.where_thicker(1)
    masked.hyoga.plot.bedrock_altitude(
        ax=ax, cmap='gist_earth', vmin=-3000, vmax=4500)
    masked.hyoga.plot.surface_altitude_contours(ax=ax)
    masked.hyoga.plot.ice_margin(ax=ax, facecolor='w')
    ax.set_title('original')

    # plot interpolated results
    for ax, res in zip(axes[1:], resolutions):
        stride = int(res/100)
        interp = ds.hyoga.interp(topo[::stride, ::stride])
        interp.hyoga.plot.bedrock_altitude(
            ax=ax, cmap='gist_earth', vmin=-3000, vmax=4500)
        interp.hyoga.plot.surface_altitude_contours(ax=ax)
        interp.hyoga.plot.ice_margin(ax=ax, facecolor='w')
        ax.set_title('{} m'.format(res))

    # constrain original data axes limits
    axes[0].set_xlim(axes[1].get_xlim())
    axes[0].set_ylim(axes[1].get_ylim())

# show
plt.show()
