# Copyright (c) 2023, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provides a single data dictionary containing origins and geographic
bounds for the default set of modelling domains.
"""

WORLD = {

    # North America
    'Ahklun':           (60, -160, [-100e3,   -150e3,  150e3,  100e3]),
    'Nevada':           (38, -119, [-170e3,   -270e3,  120e3,  220e3]),
    'Yellowstone':      (44, -110, [-150e3,   -200e3,  150e3,  200e3]),
    'Cocuy':            (6,   -73, [-50e3,    -100e3,  150e3,  200e3]),
    'Patagonia':        (-47, -72, [-400e3,  -1000e3,  400e3, 1000e3]),

    # Europe & Africa
    'Faroe':            (62,   -7, [-120e3,   -170e3,  170e3,  120e3]),
    'Pyrenees':         (43,    1, [-250e3,   -100e3,  150e3,   50e3]),
    'Cantal':           (45,    3, [-70e3,    -100e3,  120e3,  120e3]),
    'Alps':             (46,   10, [-420e3,   -270e3,  470e3,  320e3]),
    'Prokletije':       (43,   20, [-50e3,     -90e3,   30e3,  -10e3]),
    'Bale':             (7,    40, [-70e3,     -50e3,   20e3,   50e3]),

    # Asia & Oceania
    'Himalaya':         (34,   87, [-1820e3,  -950e3, 1770e3,  850e3]),
    'Altai':            (50,   89, [-400e3,   -400e3,  400e3,  400e3]),
    'Putorana':         (69,   95, [-270e3,   -200e3,  120e3,  200e3]),
    'Transbaikal':      (56,  114, [-500e3,   -370e3,  500e3,  420e3]),
    'Akaishi':          (36,  138, [0e3,       -80e3,   30e3,  -20e3]),
    'Hidaka':           (43,  143, [-30e3,     -50e3,  -10e3,  -20e3]),
    'SouthernAlps':     (-44, 170, [-400e3,   -350e3,  400e3,  450e3]),
}
