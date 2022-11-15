# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide so-called downloader classes for various websites and data
formats as needed by hyoga. Downloader objects are callable that retrieve one
or several files from the web, store them in hyoga's cache directory, and
return a path to that file, or to the main file.
"""

import os.path
import urllib.parse
import requests
import zipfile


class Downloader:
    """A generic class to download files by url and local output path."""

    def __init__(self):
        """Create hyoga cache directory if missing."""
        # IDEA: add config parameter for cache directory
        self.cachedir = os.path.expanduser(os.path.join(
            '~', '.cache', 'hyoga'))
        os.makedirs(self.cachedir, exist_ok=True)

    def __call__(self, url, path):
        """Download file if missing and return local path."""
        # IDEA: we could split this in cutsomizable steps:
        # - url(): get the url of file to download
        # - wget(): actually download file (code below)
        # - path(): return the local file path
        #   - deflate(): extract zip file
        filepath = os.path.join(self.cachedir, path)
        if not os.path.isfile(filepath):
            os.makedirs(self.cachedir, exist_ok=True)
            with open(filepath, 'wb') as binaryfile:
                print(f"downloading {url}...")
                binaryfile.write(requests.get(url).content)
        return filepath


class BasenameDownloader(Downloader):
    """A class to download files by url and save them according to basename."""

    def __call__(self, url):
        """Download file if missing and return local path."""
        path = urllib.parse.urlparse(url).path
        path = os.path.basename(path)
        path = path.split('/')[-1]
        return super().__call__(url, path)


class OSFDownloader(Downloader):
    """A class to download files by record key from osf.io."""

    def __call__(self, record, path):
        url = 'https://osf.io/' + record + '/download'
        return super().__call__(url, path)


class ZipShapeDownloader(BasenameDownloader):
    """Download zip archive and extract shapefile and metafiles."""

    def __call__(self, url, filename):

        # download zip file if missing
        archivepath = super().__call__(url)

        # assert full shp filename was passed
        assert filename.endswith('.shp')
        stem = filename[:-4]

        # extract any missing file
        for ext in ('.dbf', '.shp', '.shx'):
            if not os.path.isfile(os.path.join(self.cachedir, stem+ext)):
                with zipfile.ZipFile(archivepath, 'r') as archive:
                    archive.extract(stem+ext, path=self.cachedir)

        # return path of shp file
        return os.path.join(self.cachedir, filename)
