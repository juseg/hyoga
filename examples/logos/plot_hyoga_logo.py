#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot hyoga logo
===============

Plot default white monochrome logo including glaciers and paleoglaciers.
"""

import matplotlib.pyplot as plt
import hyoga.open
import hyoga.plot

# initialize figure
fig = plt.figure(figsize=(9.6, 3.2))
fig.patch.set_facecolor('0.25')  # ignored by transparent=True
ax = fig.add_axes([17/48, 1/32, 14/48, 13/16])
ax.patch.set_facecolor('none')
ax.set_xlim((-6.4e6, 6.4e6))
ax.set_ylim((-6.4e6, 6.4e6))
ax.axis('off')

# add continents and glaciers
crs = '+a=6378137 +proj=ortho +lon_0=-45 +lat_0=90'
hyoga.open.naturalearth(
    'admin_0_countries', category='cultural', scale='110m').to_crs(crs).plot(
        ax=ax, alpha=0.25, facecolor='w')
hyoga.open.paleoglaciers('bat19').to_crs(crs).plot(
    ax=ax, alpha=0.75, facecolor='w')
hyoga.open.naturalearth('glaciated_areas', scale='50m').to_crs(crs).plot(
    ax=ax, edgecolor='w', facecolor='w')

# add text and overline
fig.text(
    1/2, 0, 'hy  ga', color='w', family='monospace', ha='center', va='bottom',
    fontsize=7/8*fig.get_window_extent().height/fig.dpi*72)
ax.fill_between(
    [5/12, 7/12], 15/16, 1, clip_on=False, facecolor='w',
    transform=fig.transFigure)

# add circle for the o
ax.add_patch(plt.Circle(
    (0, 0), 6.4e6, capstyle='round', clip_on=False, edgecolor='w',
    facecolor='none', linewidth=16))

# save static file
# fig.savefig('../../doc/_static/png/hyoga_logo.png', transparent=True)
