#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Arctic paleoglaciers
====================

Plot Batchelor et al. (2019) arctic paleoglaciers as a standalone vector map,
using a north polar stereographic coordinate system (https://epsg.io/3995).
"""

import matplotlib.pyplot as plt
import hyoga

# plot natural earth land
gdf = hyoga.open.natural_earth('land', scale='50m').to_crs('epsg:3995')
ax = gdf.plot(color='0.9')

# plot paleoglaciers
gdf = hyoga.open.paleoglaciers('bat19').to_crs('epsg:3995')
ax = gdf.plot(ax=ax, alpha=0.75)

# set title
ax.set_title('Last Glacial Maximum (Batchelor et al., 2019)')

# reasonable axes limits
ax.set_xlim(-7.2e6, 7.2e6)
ax.set_ylim(-4.8e6, 4.8e6)

# show
plt.show()
