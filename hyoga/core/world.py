# Copyright (c) 2023, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provides a single data dictionary containing origins and geographic
bounds for the default set of modelling domains.
"""

WORLD = {

    # North America
    'Kigluaik':         (65, -164, [-100e3,   -100e3,  100e3,  100e3]),
    'Ahklun':           (60, -160, [-100e3,   -150e3,  150e3,  100e3]),
    'Brooks':           (68, -150, [-400e3,   -150e3,  400e3,  150e3]),
    'Olympic':          (48, -123, [-80e3,     -40e3,   80e3,   40e3]),
    'SouthCascades':    (43, -122, [-50e3,    -150e3,   50e3,  150e3]),
    'NorthCascades':    (47, -121, [-100e3,   -110e3,  100e3,  110e3]),
    'Nevada':           (38, -119, [-170e3,   -270e3,  120e3,  220e3]),
    'Wallowa':          (44, -115, [-90e3,     -50e3,   90e3,   50e3]),
    'Yellowstone':      (44, -110, [-150e3,   -200e3,  150e3,  200e3]),
    'Uinta':            (41, -110, [-80e3,     -40e3,   80e3,   40e3]),
    'SanJuan':          (38, -107, [-100e3,    -60e3,  100e3,   60e3]),
    'Sawatch':          (40, -106, [-110e3,   -140e3,  110e3,  140e3]),

    # South America
    'SantaMarta':       (11,  -74, [-100e3,   -100e3,  100e3,  100e3]),
    'Merida':           (9,   -71, [-100e3,   -100e3,  100e3,  100e3]),
    'Cocuy':            (6,   -73, [-50e3,    -100e3,  150e3,  200e3]),
    'Sumapaz':          (5,   -74, [-100e3,   -100e3,  100e3,  100e3]),
    'Ruiz':             (5,   -75, [-100e3,   -100e3,  100e3,  100e3]),
    'Huila':            (2,   -76, [-100e3,   -100e3,  100e3,  100e3]),
    'Ecuador':          (-1,  -79, [-100e3,   -100e3,  100e3,  100e3]),
    'Peruvian':         (-11, -73, [-500e3,   -500e3,  500e3,  500e3]),
    'Patagonia':        (-40, -71, [-600e3,  -1800e3,  600e3, 1800e3]),
    'SouthGeorgia':     (-54, -37, [-170e3,    -60e3,  170e3,   60e3]),

    # Europe
    'Iceland':          (65,  -19, [-500e3,   -250e3,  500e3,  250e3]),
    'JanMayen':         (71,   -9, [-70e3,     -30e3,   70e3,   30e3]),
    'Eixe':             (42,   -7, [-100e3,   -100e3,  100e3,  100e3]),
    'Faroe':            (62,   -7, [-120e3,   -170e3,  170e3,  120e3]),
    'Cantabrian':       (43,   -5, [-100e3,   -100e3,  100e3,  100e3]),
    'Pyrenees':         (43,    1, [-250e3,   -100e3,  150e3,   50e3]),
    'Cantal':           (45,    3, [-70e3,    -100e3,  120e3,  120e3]),
    'Corsica':          (42,    9, [-100e3,   -100e3,  100e3,  100e3]),
    'Alps':             (46,   10, [-420e3,   -270e3,  470e3,  320e3]),
    'Harz':             (52,   11, [-100e3,   -100e3,  100e3,  100e3]),
    'Sumava':           (49,   14, [-100e3,   -100e3,  100e3,  100e3]),
    'Dinaric':          (43,   19, [-100e3,   -100e3,  100e3,  100e3]),
    'Tatra':            (49,   20, [-100e3,   -100e3,  100e3,  100e3]),
    'Pindus':           (40,   21, [-100e3,   -100e3,  100e3,  100e3]),
    'RilaPirin':        (42,   23, [-100e3,   -100e3,  100e3,  100e3]),
    'Carpathians':      (45,   24, [-100e3,   -100e3,  100e3,  100e3]),
    'Rodna':            (48,   25, [-100e3,   -100e3,  100e3,  100e3]),
    'Apennine':         (42,   14, [-100e3,   -100e3,  100e3,  100e3]),
    'Kackar':           (41,   41, [-90e3,     -40e3,   90e3,   40e3]),
    'Caucasus':         (43,   43, [-440e3,   -150e3,  440e3,  150e3]),

    # Africa
    'Rwenzori':         (0,    30, [-100e3,   -100e3,  100e3,  100e3]),
    'Bale':             (7,    40, [-70e3,     -50e3,   20e3,   50e3]),

    # Asia & Oceania
    'Alborz':           (36,   51, [-90e3,     -50e3,   90e3,   50e3]),
    'Urals':            (66,   63, [-100e3,   -100e3,  100e3,  100e3]),
    'Kerguelen':        (-49,  69, [-100e3,   -100e3,  100e3,  100e3]),
    'Himalaya':         (34,   87, [-1820e3,  -950e3, 1770e3,  850e3]),
    'Altai':            (50,   89, [-400e3,   -400e3,  400e3,  400e3]),
    'Putorana':         (69,   95, [-270e3,   -200e3,  120e3,  200e3]),
    'Sayan':            (53,   98, [-350e3,   -300e3,  350e3,  300e3]),
    'Khangai':          (47,  100, [-300e3,   -300e3,  300e3,  300e3]),
    'TienShan':         (42,   80, [-300e3,   -300e3,  300e3,  300e3]),
    'Transbaikal':      (56,  114, [-500e3,   -370e3,  500e3,  420e3]),
    'Stanovoy':         (55,  130, [-100e3,   +000e3,  300e3,  200e3]),
    'Verkhoyansk':      (67,  130, [-250e3,   -250e3,  250e3,  250e3]),
    'YamAlin':          (52,  135, [-100e3,   -200e3,  100e3,  200e3]),
    'Tasmania':         (-42, 146, [-30e3,     -20e3,   30e3,   20e3]),
    'Chukotka':         (61,  163, [-500e3,   -500e3,  500e3,  500e3]),
    'SouthernAlps':     (-44, 170, [-400e3,   -350e3,  400e3,  450e3]),
}
