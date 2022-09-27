#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Natural Earth subjects
======================

Plot location map and highlight particular subjects.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import hyoga.open
import hyoga.plot


# initialize figure
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.UTM(32))

# plot demo bedrock altitude
with hyoga.open.example('pism.alps.out.2d.nc') as ds:
    ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)

# add cultural elements
hyoga.plot.countries(
    ax=ax, facecolor='none', alpha=0.75, subject='Switzerland',
    subject_facecolor='tab:red')
hyoga.plot.states(
    ax=ax, facecolor='none', alpha=0.75, subject='Salzburg',
    subject_facecolor='tab:green')
hyoga.plot.country_borders(ax=ax)

# add physical elements
hyoga.plot.rivers(
    ax=ax, subject='Po', subject_edgecolor='tab:blue', subject_linewidth=2)
hyoga.plot.lakes(
    ax=ax, subject='Lago di Garda', subject_facecolor='tab:blue')
hyoga.plot.coastline(ax=ax)

# show
plt.show()
