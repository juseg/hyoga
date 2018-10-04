#!/usr/bin/env python
# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot Hokkaido within Japan location map.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartowik.naturalearth as cne


# Main program
# ------------

# initialize figure
fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.PlateCarree())
ax.set_extent((138.5, 146.5, 40.5, 46.5), crs=ax.projection)
ax.background_patch.set_facecolor('#c6ecff')  # drawing oceans is very slow

# add cultural elements
cne.add_countries(ax, subject='Japan', subject_facecolor='#f6e1b9')
cne.add_states(ax, subject='Hokkaidō', facecolor='none')
cne.add_state_borders(ax)
cne.add_country_borders(ax)

# add physical elements
cne.add_rivers(ax)
cne.add_lakes(ax)
cne.add_coastline(ax)

# show
plt.show()
