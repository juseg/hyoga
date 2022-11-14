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


class SimpleDownloader:
    """A class to download files by url and optionally output name."""

    def __init__(self):
        """Create hyoga cache directory if missing."""
        # IDEA: add config parameter for cache directory
        self.cachedir = os.path.expanduser(os.path.join(
            '~', '.cache', 'hyoga'))
        os.makedirs(self.cachedir, exist_ok=True)

    def __call__(self, url, filename=None):
        """Download file if missing and return local path."""
        if filename is None:
            filename = urllib.parse.urlparse(url).path
            filename = os.path.basename(filename)
            filename = filename.split('/')[-1]
        filepath = os.path.join(self.cachedir, filename)
        if not os.path.isfile(filepath):
            os.makedirs(self.cachedir, exist_ok=True)
            with open(filepath, 'wb') as binaryfile:
                print(f"downloading {url}...")
                binaryfile.write(requests.get(url).content)
        return filepath
