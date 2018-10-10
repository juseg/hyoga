# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Wikipedia color and linestyle conventions.
"""

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


# Topographic colormaps
# ---------------------

BATHYMETRIC = mcolors.LinearSegmentedColormap.from_list('Bathymetric', [
    (1-6000/6000, COLORS['bathy09']),  # 9000 6000 3000 dark blue
    (1-3000/6000, COLORS['bathy08']),  # 4500 3000 1500
    (1-2000/6000, COLORS['bathy07']),  # 3000 2000 1000
    (1-1500/6000, COLORS['bathy06']),  # 2250 1500  750
    (1-1000/6000, COLORS['bathy05']),  # 1500 1000  500
    (1-750/6000, COLORS['bathy04']),   # 1125  750  325
    (1-500/6000, COLORS['bathy03']),   # '750  500  250
    (1-250/6000, COLORS['bathy02']),   # '375  250  125
    (1-100/6000, COLORS['bathy01']),   # '150  100   50
    (1-0/6000, COLORS['bathy00']),     # '  0    0    0 light blue
])

TOPOGRAPHIC = mcolors.LinearSegmentedColormap.from_list('Topographic', [
    (0/9000, COLORS['topog01']),     # '   0     0    0    0    0
    (50/9000, COLORS['topog02']),    # ' 100    75   50   33   25 dark green
    (100/9000, COLORS['topog03']),   # ' 200   150  100   67   50
    (250/9000, COLORS['topog04']),   # ' 500   375  250  167  125
    (500/9000, COLORS['topog05']),   # '1000   750  500  333  250
    (750/9000, COLORS['topog06']),   # '1500  1125  750  500  375
    (1000/9000, COLORS['topog07']),  # '2000  1500 1000  667  500 light yellow
    (1500/9000, COLORS['topog08']),  # '3000  2250 1500 1000  750
    (2000/9000, COLORS['topog09']),  # '4000  3000 2000 1333 1000
    (2500/9000, COLORS['topog10']),  # '5000  3750 2500 1667 1250
    (3000/9000, COLORS['topog11']),  # '6000  4500 3000 2000 1500
    (3500/9000, COLORS['topog12']),  # '7000  5250 3500 2333 1750
    (4000/9000, COLORS['topog13']),  # '8000  6000 4000 2667 2000
    (4500/9000, COLORS['topog14']),  # '9000  6750 4500 3000 2550 dark brown
    (5000/9000, COLORS['topog15']),  # 10000  7500 5000 3333 2500
    (6000/9000, COLORS['topog16']),  # 12000  9000 6000 4000 3000
    (7000/9000, COLORS['topog17']),  # 14000 10500 7000 4667 3500
    (8000/9000, COLORS['topog18']),  # 16000 12000 8000 5333 4000
    (9000/9000, COLORS['topog19']),  # 18000 13500 9000 6000 4500 light grey
])


# Colormaps dictionary
# --------------------

COLORMAPS = dict(
    Bathymetric=BATHYMETRIC,
    Topographic=TOPOGRAPHIC,
)
