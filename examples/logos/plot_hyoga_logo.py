#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot hyoga logo
===============

Plot default white monochrome logo including glaciers and paleoglaciers.
"""

import matplotlib.pyplot as plt
import cartopy
import hyoga.open
import hyoga.plot

# initialize figure
fig = plt.figure(figsize=(9.6, 3.2))
fig.patch.set_facecolor('0.25')  # ignored by transparent=True
ax = fig.add_axes(
    [17/48, 1/32, 14/48, 13/16], projection=cartopy.crs.Orthographic(
        central_longitude=-45, central_latitude=90))
ax.patch.set_facecolor('none')
ax.spines['geo'].set(capstyle='round', edgecolor='w', linewidth=16)

# ax.set_extent does not work well with ortho proj
ax.set_xlim((-6.4e6, 6.4e6))
ax.set_ylim((-6.4e6, 6.4e6))

# add continents and glaciers
hyoga.plot.countries(ax=ax, alpha=0.25, facecolor='w', scale='110m')
hyoga.plot.paleoglaciers(ax=ax, alpha=0.75, facecolor='w', source='bat19')
hyoga.plot.glaciers(ax=ax, edgecolor='w', facecolor='w', scale='50m')

# add text and overline
fig.text(
    1/2, 0, 'hy  ga', color='w', family='monospace', ha='center', va='bottom',
    fontsize=7/8*fig.get_window_extent().height/fig.dpi*72)
ax.fill_between(
    [5/12, 7/12], 15/16, 1, clip_on=False, facecolor='w',
    transform=fig.transFigure)

# save static file
# fig.savefig('../../doc/_static/png/hyoga_logo.png', transparent=True)
