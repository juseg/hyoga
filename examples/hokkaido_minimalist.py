#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot Hokkaido minimalist transparent map.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartowik.naturalearth as cne


# initialize figure
fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.UTM(54))
ax.set_extent((250e3, 1050e3, 4500e3, 5100e3), crs=ax.projection)
ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)

# add cultural elements
cne.add_states(ax=ax, subject='Hokkaidō', facecolor='none',
               subject_facecolor='none', subject_edgecolor='k')

# show
plt.show()
