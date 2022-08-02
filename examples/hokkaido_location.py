#!/usr/bin/env python
# Copyright (c) 2018, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot Hokkaido within Japan location map.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartowik.naturalearth as cne


# initialize figure
fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.UTM(54))
ax.set_extent((250e3, 1050e3, 4500e3, 5100e3), crs=ax.projection)
ax.background_patch.set_facecolor('#c6ecff')  # drawing oceans is very slow

# add cultural elements
cne.add_countries(ax=ax, subject='Japan', subject_facecolor='#f6e1b9')
cne.add_states(ax=ax, subject='Hokkaidō', facecolor='none')
cne.add_state_borders(ax=ax)
cne.add_country_borders(ax=ax)

# add physical elements
cne.add_rivers(ax=ax)
cne.add_lakes(ax=ax)
cne.add_coastline(ax=ax)

# show
plt.show()
