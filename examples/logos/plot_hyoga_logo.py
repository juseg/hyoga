#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Plot hyoga logo."""

import matplotlib.pyplot as plt
import cartopy
import hyoga.demo
import hyoga.plot

# initialize figure
fig = plt.figure(figsize=(9.6, 3.2))
fig.patch.set_alpha(0)
ax = fig.add_axes([17/48, 0, 14/48, 7/8], projection=cartopy.crs.Orthographic(
        central_longitude=-45, central_latitude=90))
ax.patch.set_facecolor('tab:blue')
ax.spines['geo'].set_edgecolor('none')

# ax.set_extent does not work well with ortho proj
ax.set_xlim((-6.4e6, 6.4e6))
ax.set_ylim((-6.4e6, 6.4e6))

# add continents and glaciers
hyoga.plot.countries(ax=ax, alpha=0.25, facecolor='w', scale='110m')
hyoga.plot.paleoglaciers(ax=ax, alpha=0.75, facecolor='w', source='bat19')
hyoga.plot.glaciers(ax=ax, edgecolor='w', facecolor='w', scale='50m')

# add text and overline
fontsize = 7/8 * fig.get_window_extent().height / fig.dpi * 72
kwargs = dict(color='tab:blue', fontsize=fontsize, va='bottom')
fig.text(1/3, 0, 'hy', ha='right', **kwargs)
fig.text(2/3, 0, 'ga', ha='left', **kwargs)
ax.fill_between([5/12, 7/12], 15/16, 1, clip_on=False, facecolor='tab:blue',
                transform=fig.transFigure)

# save static file
# fig.savefig('../../doc/_static/hyoga_logo.png')
