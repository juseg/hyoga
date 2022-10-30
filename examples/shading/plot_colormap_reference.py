#!/usr/bin/env python
# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Colormap reference
==================

Plot hyoga altitude and relief colormaps.
"""

import numpy as np
import matplotlib.pyplot as plt
import hyoga  # register colormaps, pylint: disable=unused-import

# initialize figure
fig, axes = plt.subplots(nrows=5)
fig.subplots_adjust(left=0.2)

# prepare gradient image
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# plot background pattern and color gradients
colormaps = ['Bathymetric', 'Topographic', 'Elevational', 'Matte', 'Glossy']
for ax, name in zip(axes, colormaps):
    ax.patch.set(hatch='..', edgecolor='0.5')
    ax.imshow(gradient, aspect='auto', cmap=name)
    ax.text(-8, .5, name, va='center', ha='right', fontsize=10)
    ax.set(xticks=[], yticks=[])

# set axes properties
axes[0].set_title('Hyoga colormaps')

# show
plt.show()
