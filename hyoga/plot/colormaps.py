# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module defines new altitude and relief-shading colormaps for matplotlib.
The color definitions are based on Wikipedia's "WikiProject Maps" cartographic
[conventions](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Maps/Conventions)
for topographic maps.
"""

import matplotlib as mpl

# color sequences dictionary
SEQUENCES = {

    # bathymetric levels optimized for [6000, 0] and example rescaling
    'Bathymetric': [(1+level/6000, color) for (level, color) in [
        (-6000, '#71ABD8'),     # 9000 6000 3000 dark blue
        (-3000, '#79B2DE'),     # 4500 3000 1500
        (-2000, '#84B9E3'),     # 3000 2000 1000
        (-1500, '#8DC1EA'),     # 2250 1500  750
        (-1000, '#96C9F0'),     # 1500 1000  500
        (-750,  '#A1D2F7'),     # 1125  750  325
        (-500,  '#ACDBFB'),     # :750  500  250
        (-250,  '#B9E3FF'),     # :375  250  125
        (-100,  '#C6ECFF'),     # :150  100   50
        (-0,    '#D8F2FE')]],   # :  0    0    0 light blue

    # topographic levels optimized for [0, 9000] and example rescaling
    'Topographic': [(level/9000, color) for (level, color) in [
        (0,     '#ACD0A5'),     # :   0     0    0    0    0
        (50,    '#94BF8B'),     # : 100    75   50   33   25 dark green
        (100,   '#A8C68F'),     # : 200   150  100   67   50
        (250,   '#BDCC96'),     # : 500   375  250  167  125
        (500,   '#D1D7AB'),     # :1000   750  500  333  250
        (750,   '#E1E4B5'),     # :1500  1125  750  500  375
        (1000,  '#EFEBC0'),     # :2000  1500 1000  667  500 light yellow
        (1500,  '#E8E1B6'),     # :3000  2250 1500 1000  750
        (2000,  '#DED6A3'),     # :4000  3000 2000 1333 1000
        (2500,  '#D3CA9D'),     # :5000  3750 2500 1667 1250
        (3000,  '#CAB982'),     # :6000  4500 3000 2000 1500
        (3500,  '#C3A76B'),     # :7000  5250 3500 2333 1750
        (4000,  '#B9985A'),     # :8000  6000 4000 2667 2000
        (4500,  '#AA8753'),     # :9000  6750 4500 3000 2550 dark brown
        (5000,  '#AC9A7C'),     # 10000  7500 5000 3333 2500
        (6000,  '#BAAE9A'),     # 12000  9000 6000 4000 3000
        (7000,  '#CAC3B8'),     # 14000 10500 7000 4667 3500
        (8000,  '#E0DED8'),     # 16000 12000 8000 5333 4000
        (9000,  '#F5F4F2')]]}   # 18000 13500 9000 6000 4500 light grey

# call update so we can access bathy and topo colors
SEQUENCES.update({

    # elevational levels with sea level in the middle
    'Elevational': (
        [(0.0+0.5*l, c) for (l, c) in SEQUENCES['Bathymetric']] +
        [(0.5+0.5*l, c) for (l, c) in SEQUENCES['Topographic']]),

    # matte hillshading
    'Matte': [
        (0.0, '#00000000'),     # transparent black
        (1.0, '#000000ff')],    # solid black

    # glossy hillshading
    'Glossy': [
        (0.0, '#ffffffff'),     # solid white
        (0.5, '#ffffff00'),     # transparent white
        (0.5, '#00000000'),     # transparent black
        (1.0, '#000000ff')]})   # solid black

# colormaps dictionary (4k colors to avoid striping in plains)
COLORMAPS = {
    name: mpl.colors.LinearSegmentedColormap.from_list(
        name, colors, N=4096) for name, colors in SEQUENCES.items()}

# topographic depressions
COLORMAPS['Topographic'].set_under('#A7DFD2')

# register colormaps with matplotlib
if mpl.__version__ >= '3.5':
    for cmap in COLORMAPS.values():
        mpl.colormaps.register(cmap)
else:
    for cmap in COLORMAPS.values():
        mpl.cm.register_cmap(cmap=cmap)
