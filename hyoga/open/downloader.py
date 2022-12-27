# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide so-called downloader classes for various websites and data
formats as needed by hyoga. Downloader objects are callable that retrieve one
or several files from the web, store them in hyoga's cache directory, and
return a path to that file, or to the main file.
"""

import os.path
import zipfile
import requests


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
        """See class documentation for actual signature.

        Parameters
        ----------
        *args :
            Positional arguments are passed to :meth:`url` and :meth:`path`.
            These two methods need to have compatible signatures.
        **kwargs :
            Keyword arguments are passed to :meth:`get` to alter the download
            recipe. This is used to provide a member filename in an archive.
        """
        url = self.url(*args)
        path = self.path(*args)
        if not self.check(path):
            self.get(url, path, **kwargs)
        return path

    def url(self, *args):
        """Return url of file to download."""
        return args[0]

    def path(self, *args):
        """Return local path of downloaded file."""
        return args[1]

    def check(self, path):
        """Check whether file is present."""
        return os.path.isfile(path)

    def get(self, url, path):
        """Download online `url` to local `path`."""

        # create directory if missing
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # open url and raise any http error
        with requests.get(url, stream=True, timeout=5) as request:
            request.raise_for_status()

            # download file chunks
            print(f"downloading {url}...")
            with open(path, 'wb') as binaryfile:
                for chunk in request.iter_content(chunk_size=1024**2):
                    binaryfile.write(chunk)


class CacheDownloader(Downloader):
    """A downloader that stores files in hyoga's cache directory.

    Call parameters
    ---------------
    url : str
        The url of the file to download
    path : str
        The path of the downloaded file relative to the cache directory.
    """

    def path(self, *args):
        path = super().path(*args)
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(
            os.path.expanduser('~'), '.cache'))
        return os.path.join(xdg_cache, 'hyoga', path)


class OSFDownloader(CacheDownloader):
    """A class to download files by record key from osf.io.

    Call parameters
    ---------------
    record : str
        Record key of the file to download on osf.io.
    path : str
        The path of the downloaded file relative to the cache directory.
    """

    def url(self, *args):
        record = super().url(*args)
        return 'https://osf.io/' + record + '/download'


class ArchiveDownloader(CacheDownloader):
    """A base class to download archives and extract member files.

    Call parameters
    ---------------
    url : str
        The url of the file to download
    path : str
        The path of the extracted file relative to the cache directory.
    member : str, optional
        Member file to extract from archive, default to basename of ``path``.
    """

    def get(self, url, path, member=None):

        # save archive as named online
        outdir, basename = os.path.split(path)
        # FIXME GEBCO arvhive is just named 'zip'
        archivepath = os.path.join(outdir, url.rstrip('/').split('/')[-1])

        # download it only if missing
        if not super().check(archivepath):
            super().get(url, archivepath)

        # by default assume member name is path basename
        member = member or basename

        # this needs to be implemented in subclasses
        self.deflate(archivepath, member, outdir)

    def deflate(self, archivepath, member, outdir):
        """Extract member and any other needed files from the archive."""
        raise NotImplementedError("This should be implemented in subclasses.")


class ZipDownloader(ArchiveDownloader):
    """
    Download a zip archive and extract a single file.

    Call parameters
    ---------------
    url : str
        The url of the file to download
    path : str
        The path of the extracted file relative to the cache directory.
    member : str, optional
        Member file to extract from , default to the basename of ``path``.
    """

    def deflate(self, archivepath, member, outdir):
        with zipfile.ZipFile(archivepath, 'r') as archive:
            archive.extract(member, path=outdir)


class ShapeZipDownloader(ArchiveDownloader):
    """A downloader that extracts shapefiles and metafiles from zip archives.

    Call parameters
    ---------------
    url : str
        The url of the file to download
    path : str
        The path of the extracted file relative to the cache directory.
    member : str, optional
        Member file to extract from , default to the basename of ``path``.
    """

    extensions = ('.shp', '.dbf', '.prj', '.shx')

    def check(self, path):
        stem, ext = os.path.splitext(path)
        supercheck = super().check  # call super() outside generator
        return all(supercheck(stem+ext) for ext in self.extensions)

    def deflate(self, archivepath, member, outdir):
        stem, ext = os.path.splitext(member)
        with zipfile.ZipFile(archivepath, 'r') as archive:
            for ext in self.extensions:
                archive.extract(stem+ext, path=outdir)


class NaturalEarthDownloader(ShapeZipDownloader):
    """A downloader for Natural Earth Data.

    Call parameters
    ---------------
    scale : {'10m', '50m', '110m'}
        Natural Earth data scale.
    category : {'cultural', 'physical'}
        Natural Earth data category.
    theme : str or iterable
        Natural Earth data theme.
    """

    def url(self, *args):
        scale, category, theme = args
        return (
            f'https://naturalearth.s3.amazonaws.com/{scale}_{category}/'
            f'ne_{scale}_{theme}.zip')

    def path(self, *args):

        # this is where cartopy stores the same data
        scale, category, theme = args
        xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.join(
            os.path.expanduser('~'), '.local', 'share'))
        cartopy_stem = os.path.join(
            xdg_data_home, 'cartopy', 'shapefiles', 'natural_earth',
            category, f'ne_{scale}_{theme}')

        # if all files are there, return this path
        extensions = ('.shp', '.dbf', '.prj', '.shx')
        if all(os.path.isfile(cartopy_stem+ext) for ext in extensions):
            return cartopy_stem + '.shp'

        # otherwise return path relative to hyoga cache
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(
            os.path.expanduser('~'), '.cache'))
        path = os.path.join(
            xdg_cache, 'hyoga', 'natural_earth', f'{scale}_{category}',
            f'ne_{scale}_{theme}.shp')
        return path
