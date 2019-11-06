#!/usr/bin/env python
# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot Hokkaido topographic map.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartowik.naturalearth as cne
import cartowik.shadedrelief as csr


# initialize figure
fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.UTM(54))
ax.set_extent((250e3, 1050e3, 4500e3, 5100e3), crs=ax.projection)

# add relief maps
csr.add_bathymetry('external/cleantopo2.tif', offset=10701.0)
csr.add_multishade('external/cleantopo2.tif')
csr.add_topography('external/srtm.tif', vmax=4500)
csr.add_multishade('external/srtm.tif')

# add physical elements
cne.add_rivers(ax=ax)
cne.add_lakes(ax=ax)
cne.add_coastline(ax=ax)

# add cultural elements
cne.add_states(ax=ax, facecolor='w', alpha=0.5,
               subject='Hokkaidō', subject_facecolor='none')
cne.add_state_borders(ax=ax)
cne.add_country_borders(ax=ax)

# show
plt.show()
