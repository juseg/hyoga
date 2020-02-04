# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Wikipedia color and linestyle conventions.
"""

import numpy as np
import matplotlib.colors as mcolors


# Wikipedia color conventions
# ---------------------------

COLORS = dict(
    # location maps
    names='#000000',    # toponymes
    borders='#646464',  # and country labels
    subject='#FEFEE9',  # primary
    context='#F6E1B9',  # secondary
    outside='#E0E0E0',  # off-topic
    rivers='#0978AB',   # and coasts
    lakes='#C6ECFF',    # and seas
    # topographic contours
    topog19='#F5F4F2',  # light gray
    topog18='#E0DED8',
    topog17='#CAC3B8',
    topog16='#BAAE9A',
    topog15='#AC9A7C',
    topog14='#AA8753',  # dark brown
    topog13='#B9985A',
    topog12='#C3A76B',
    topog11='#CAB982',
    topog10='#D3CA9D',
    topog09='#DED6A3',
    topog08='#E8E1B6',
    topog07='#EFEBC0',  # light yellow
    topog06='#E1E4B5',
    topog05='#D1D7AB',
    topog04='#BDCC96',
    topog03='#A8C68F',
    topog02='#94BF8B',  # dark green
    topog01='#ACD0A5',
    topog00='#A7DFD2',  # depressions
    # bathymetry contours
    bathy00='#D8F2FE',  # light blue
    bathy01='#C6ECFF',
    bathy02='#B9E3FF',
    bathy03='#ACDBFB',
    bathy04='#A1D2F7',
    bathy05='#96C9F0',
    bathy06='#8DC1EA',
    bathy07='#84B9E3',
    bathy08='#79B2DE',
    bathy09='#71ABD8',  # dark blue
)

CLISTS = dict(
    Bathymetric=[COLORS['bathy{:02d}'.format(9-i)] for i in range(10)],
    Topographic=[COLORS['topog{:02d}'.format(i)] for i in range(19)],
)


# Contour level conventions
# -------------------------

LEVELS = dict(
    Bathymetric=[  # -color-  -example linear rescaling-
        -6000,     # bathy09   9000 6000 3000 dark blue
        -3000,     # bathy08   4500 3000 1500
        -2000,     # bathy07   3000 2000 1000
        -1500,     # bathy06   2250 1500  750
        -1000,     # bathy05   1500 1000  500
        -750,      # bathy04   1125  750  325
        -500,      # bathy03    750  500  250
        -250,      # bathy02    375  250  125
        -100,      # bathy01    150  100   50
        -0,        # bathy00      0    0    0 light blue
    ],
    Topographic=[  # -color-  -example linear rescaling-
        0,         # topog01      0     0    0    0    0
        50,        # topog02    100    75   50   33   25 dark green
        100,       # topog03    200   150  100   67   50
        250,       # topog04    500   375  250  167  125
        500,       # topog05   1000   750  500  333  250
        750,       # topog06   1500  1125  750  500  375
        1000,      # topog07   2000  1500 1000  667  500 light yellow
        1500,      # topog08   3000  2250 1500 1000  750
        2000,      # topog09   4000  3000 2000 1333 1000
        2500,      # topog10   5000  3750 2500 1667 1250
        3000,      # topog11   6000  4500 3000 2000 1500
        3500,      # topog12   7000  5250 3500 2333 1750
        4000,      # topog13   8000  6000 4000 2667 2000
        4500,      # topog14   9000  6750 4500 3000 2550 dark brown
        5000,      # topog15  10000  7500 5000 3333 2500
        6000,      # topog16  12000  9000 6000 4000 3000
        7000,      # topog17  14000 10500 7000 4667 3500
        8000,      # topog18  16000 12000 8000 5333 4000
        9000,      # topog19  18000 13500 9000 6000 4500 light grey
    ],
)


# Cartowik colormaps
# ------------------

# topographic colormaps

BATHYMETRIC = mcolors.LinearSegmentedColormap.from_list(
    'Bathymetric', list(zip([1+l/6000 for l in LEVELS['Bathymetric']],
                            CLISTS['Bathymetric'])), N=4096)

TOPOGRAPHIC = mcolors.LinearSegmentedColormap.from_list(
    'Topographic', list(zip([l/9000 for l in LEVELS['Topographic']],
                            CLISTS['Topographic'])), N=4096)
TOPOGRAPHIC.set_under(COLORS['topog00'])

ELEVATIONAL = mcolors.LinearSegmentedColormap.from_list('Elevational', [
    *BATHYMETRIC(np.linspace(0, 1, 2048)),
    *TOPOGRAPHIC(np.linspace(0, 1, 2048)),
], N=4096)

# relief shading colormaps

SHADES = mcolors.LinearSegmentedColormap.from_list('Shades', [
    (0.0, '#00000000'),  # transparent black
    (1.0, '#000000ff'),  # solid black
])

SHINES = mcolors.LinearSegmentedColormap.from_list('Shines', [
    (0.0, '#ffffffff'),  # solid white
    (0.5, '#ffffff00'),  # transparent white
    (0.5, '#00000000'),  # transparent black
    (1.0, '#000000ff'),  # solid black
])

# colormaps dictionary

COLORMAPS = dict(
    Bathymetric=BATHYMETRIC,
    Topographic=TOPOGRAPHIC,
    Elevational=ELEVATIONAL,
    Shades=SHADES,
    Shines=SHINES,
)
