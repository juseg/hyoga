#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Alpine paleoglaciers
====================

Plot Ehlers et al. (2011) global paleoglacier data on top of gridded Alpine
topographic data, whose coordinate system is read from an netCDF attribute.
"""

import matplotlib.pyplot as plt
import hyoga

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
    ax = ds.hyoga.plot.paleoglaciers(alpha=0.75)

# set title
ax.set_title('Last Glacial Maximum (Ehlers et al., 2011)')

# show
plt.show()
