# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains utils to download demonstration data needed to plot
examples included in the documentation. There is currently only one function
but in the future more data may be dowloaded to demonstrate plotting time
series and plotting output from other models.
"""

import os.path
import requests


def gridded():
    """Download Alps public gridded data from Zenodo, return path."""
    filename = 'alpcyc.1km.epic.pp.ex.1ka.nc'
    if not os.path.isfile(filename):
        req = requests.get('https://zenodo.org/record/3604142/files/'+filename)
        with open(filename, 'wb') as binaryfile:
            binaryfile.write(req.content)
    return filename
