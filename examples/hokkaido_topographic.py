#!/usr/bin/env python
# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot Hokkaido within Japan location map.
"""

import rasterio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartowik.naturalearth as cne


# Main program
# ------------

# initialize figure
fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.PlateCarree())
ax.set_extent((138.5, 146.5, 40.5, 46.5), crs=ax.projection)

# plot bathymetry
with rasterio.open('external/CleanTOPO2.tif') as dataset:
    bounds = dataset.bounds
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    data = dataset.read(1)
    ax.imshow(data, cmap='Greys', extent=extent, interpolation='nearest',
              origin='upper', transform=ax.projection)

# add physical elements
cne.add_rivers(ax)
cne.add_lakes(ax)
cne.add_coastline(ax)

# add cultural elements
cne.add_states(ax, facecolor='w',  # FIXME alpha=0.5,
               subject='Hokkaidō', subject_facecolor='none')
cne.add_state_borders(ax)
cne.add_country_borders(ax)

# show
plt.show()
