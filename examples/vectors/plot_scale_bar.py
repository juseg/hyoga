#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Scale bars
==========

Plot scale bars with different styles.
"""

import matplotlib.pyplot as plt
import hyoga

# open demo data
with hyoga.open.example('pism.alps.in.boot.nc') as ds:

    # plot model output
    ds.hyoga.plot.bedrock_altitude(vmin=0)

    # custom size
    ds.hyoga.plot.scale_bar(loc='upper center', size=200e3)

    # custom style
    ds.hyoga.plot.scale_bar(loc='lower left', color='tab:red', marker='o')

    # custom label
    ds.hyoga.plot.scale_bar(loc='lower center', label='hundred kilometers')

    # default scale bar
    ds.hyoga.plot.scale_bar()


# set title
plt.title('Scale bars')

# show
plt.show()
