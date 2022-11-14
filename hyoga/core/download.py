# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide a function to download sample data needed to plot examples
included in the documentation. There are currently only few files available
but in the future more data may be dowloaded to demonstrate plotting time
series and plotting output from other models.
"""

import os.path
import urllib.parse
import requests


def _download(url, filename=None):
    """Download a file from the web, store in cache dir and return path."""
    cachedir = os.path.expanduser(os.path.join('~', '.cache', 'hyoga'))
    if filename is None:
        filename = urllib.parse.urlparse(url).path
        filename = os.path.basename(filename)
        filename = filename.split('/')[-1]
    filepath = os.path.join(cachedir, filename)
    if not os.path.isfile(filepath):
        os.makedirs(cachedir, exist_ok=True)
        with open(filepath, 'wb') as binaryfile:
            print(f"downloading {url}...")
            binaryfile.write(requests.get(url).content)
    return filepath
