# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide so-called downloader classes for various websites and data
formats as needed by hyoga. Downloader objects are callable that retrieve one
or several files from the web, store them in hyoga's cache directory, and
return a path to that file, or to the main file.
"""

import os.path
import requests
import zipfile


class Downloader:
    """A callable that downloads a file and returns its path when called.

    This is a base class for callable downloaders. Customization can be done by
    subclassing and overwriting the following methods:

    * :meth:`url`: return the url of file to download.
    * :meth:`path`: return local path of downloaded file.
    * :meth:`check`: check whether file is present or valid.
    * :meth:`get`: actually download file (and any meta file).

    Call parameters
    ---------------
    url : str
        The url of the file to download.
    path : str
        The local path of the downloaded file.

    Returns
    -------
    path : str
        The local path of the downloaded file.
    """

    def __call__(self, *args, **kwargs):
        """See class documentation for actual signature."""
        url = self.url(*args, **kwargs)
        path = self.path(*args, **kwargs)
        if not self.check(path):
            self.get(url, path, **kwargs)
        return path

    def url(self, url, path):
        """Return url of file to download."""
        return url

    def path(self, url, path):
        """Return local path of downloaded file."""
        return path

    def check(self, path):
        """Check whether file is present."""
        return os.path.isfile(path)

    def get(self, url, path):
        """Download online `url` to local `path`."""

        # create directory if missing
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # download file
        with open(path, 'wb') as binaryfile:
            print(f"downloading {url}...")
            binaryfile.write(requests.get(url).content)


class CacheDownloader(Downloader):
    """A downloader that stores files in hyoga's cache directory.

    Call parameters
    ---------------
    url:
        The url of the file to download
    path:
        The path of the downloaded file relative to the cache directory.
    """

    def path(self, url, path):
        """Return path of downloaded file relative to the cache directory."""
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(
            os.path.expanduser('~'), '.cache'))
        return os.path.join(xdg_cache, 'hyoga', path)


class OSFDownloader(CacheDownloader):
    """A class to download files by record key from osf.io.

    Call parameters
    ---------------
    record:
        Record key of the file to download on osf.io.
    path:
        The path of the downloaded file relative to the cache directory.
    """

    def url(self, record, path):
        """Return osf.io url from record key."""
        return 'https://osf.io/' + record + '/download'


class ArchiveDownloader(CacheDownloader):
    """A base class to download archives and extract member files."""

    def get(self, url, path, member=None):

        # save archive as named online
        outdir, basename = os.path.split(path)
        archivepath = os.path.join(outdir, url.split('/')[-1])

        # download it only if missing
        if not super().check(archivepath):
            super().get(url, archivepath)

        # by default assume member name is path basename
        member = member or basename

        # this needs to be implemented in subclasses
        self.deflate(archivepath, member, outdir)


class ShapeZipDownloader(ArchiveDownloader):
    """Download zip archive and extract shapefile and metafiles."""

    def deflate(self, archivepath, member, outdir):
        """Extract shapefile and companion files from zip archive."""
        stem, ext = os.path.splitext(member)
        with zipfile.ZipFile(archivepath, 'r') as archive:
            for ext in ('.shp', '.dbf', '.prj', '.shx'):
                archive.extract(stem+ext, path=outdir)


class NaturalEarthDownloader(ShapeZipDownloader):

    def __call__(self, scale, category, theme):

        # this is where cartopy stores the same data
        xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.join(
            os.path.expanduser('~'), '.local', 'share'))
        cartopy_stem = os.path.join(
            xdg_data_home, 'cartopy', 'shapefiles', 'natural_earth',
            category, f'ne_{scale}_{theme}')

        # if all files are there, return this path
        extensions = ('.shp', '.dbf', '.prj', '.shx')
        if all(os.path.isfile(cartopy_stem+ext) for ext in extensions):
            return cartopy_stem + '.shp'

        # otherwise we want a ZipShapeDownloader
        return super().__call__(
            f'https://naturalearth.s3.amazonaws.com/{scale}_{category}/'
            f'ne_{scale}_{theme}.zip',
            f'natural_earth/{scale}_{category}/ne_{scale}_{theme}.zip',
            f'ne_{scale}_{theme}.shp')
