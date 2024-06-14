# Copyright (c) 2024, Julien Seguinot (juseg.dev)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module provide so-called aggregator classes for computing multiyear means
and standard deviations needed by hyoga. Aggregator objects are callables that
may trigger downloads, open multi-file datasets, aggregate statistics, store
them in hyoga's cache directory, and return a path to that file.
"""

import os.path
import xarray as xr
import hyoga.open.downloader


class Aggregator():
    """A callable that aggregates input files and returns an output path.

    This is a base class for callable aggregator. Customization can be done by
    subclassing and overwriting the following methods:

    * :meth:`inputs`: return local paths of input files.
    * :meth:`output`: return local path of aggregated file.
    * :meth:`check`: check whether output file is present or valid.
    * :meth:`aggregate`: actually aggregate the data from input files.

    Call parameters
    ---------------
    inputs : str
        A list of paths of files to aggregate.
    output : str
        The local path of the aggregated file.

    Returns
    -------
    output : str
        The local path of the aggregated file.
    """

    def __call__(self, *args, **kwargs):
        """See class documentation for actual signature.

        Parameters
        ----------
        *args :
            Positional arguments passed to :meth:`inputs` and :meth:`output`.
            These two methods need to have compatible signatures.
        **kwargs :
            Keyword arguments are passed to :meth:`aggregate` to alter the
            aggregation recipe. This is used to provide a custom function.
        """
        inputs = self.inputs(*args)
        output = self.output(*args)
        if not self.check(output):
            self.aggregate(inputs, output, **kwargs)
        return output

    def inputs(self, *args):
        """Return local paths of input files."""
        return args[0]

    def output(self, *args):
        """Return local path of aggregated file."""
        return args[1]

    def check(self, output):
        """Check whether output file is present."""
        return os.path.isfile(output)

    def aggregate(self, inputs, output, recipe='avg'):
        """Aggregate `inputs` into `output` file."""

        # open inputs as multi-file dataset
        with xr.open_mfdataset(
                inputs, chunks={'lat': 300, 'lon': 300},
                preprocess=lambda ds: ds.assign(
                    lat=ds.lat.astype('f4'), lon=ds.lon.astype('f4')),
                # parallel=False,
                ) as ds:
            ds = getattr(
                ds, recipe.replace('avg', 'mean'))('time', keep_attrs=True)

            # FIXME implement proper tiling
            ds = ds.sel(lon=slice(5, 10), lat=slice(43, 48))

            # store output as netcdf and return path
            print(f"aggregating {output} ...")
            ds.to_netcdf(output, compute=False).compute()
            return output


# IDEA: implement intermediate TiledAggregator
class TiledAggregator(Aggregator):
    """An aggregator that splits global data split into 30x30 degree tiles.

    Call parameters
    ---------------
    inputs : str
        A list of paths of files to aggregate.
    pattern : str
        A format string for the aggregated tile paths.

    Returns
    -------
    output : str
        The local paths of the aggregated files.
    """

    def pattern(self, *args):
        """Return aggregated tile path pattern as a format string."""
        raise NotImplementedError("This should be implemented in subclasses.")


class CW5E5TiledAggregator(Aggregator):
    """An aggregator to compute CHELSA-W5E5 climatologies from daily means.

    Call parameters
    ---------------
    variable : 'tasmax', 'tas', 'tasmin', 'rsds', 'pr'
        The short name for the CHELSA-W5E5 variable aggregated among:
        - daily mean precipitation ('pr', kg m-2 s-1),
        - daily mean surface downwelling shortwave dadiation ('rsds', W m-2),
        - daily mean near-surface air temperature ('tas', K),
        - daily maximum near surface air temperature ('tasmax', K),
        - daily minimum near surface air temperature ('tasmin', K).
    start : int
        The aggregation start year between 1979 and 2016.
    end : int
        The aggregation end year between 1979 and 2016.
    month : int
        The month for which data is downloaded data between 1 and 12.
    """

    def _get_all_coords(self):
        """Return corner coordinates for all tiles."""
        # FIXME loop globally
        return ((lat, lon) for lat in (0, 30) for lon in (0, 30))

    def _get_tile_path(self, pattern, lat, lon):
        """Return tile path from pattern and corner coordinates."""
        llat = f'{'n' if (lat >= 0) else 's'}{abs(lat):02d}'
        llon = f'{'e' if (lon >= 0) else 'w'}{abs(lon):02d}'
        return pattern.format(llat+llon)

    def inputs(self, *args):
        variable, start, end, month = args
        downloader = hyoga.open.downloader.CW5E5DailyDownloader()
        years = range(start, end+1)
        paths = (downloader(variable, year, month) for year in years)
        return paths

    def _pattern(self, *args):
        variable, start, end, month = args
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(
            os.path.expanduser('~'), '.cache'))
        return os.path.join(
            xdg_cache, 'hyoga', 'cw5e5', 'clim', f'cw5e5.{variable}.mon.'
            f'{start % 100:02d}{end % 100:02d}.avg.{{}}.{month:02d}.nc')

    def output(self, *args):
        pattern = self._pattern(*args)
        coords = self._get_all_coords()
        return [self._get_tile_path(pattern, *latlon) for latlon in coords]

    def check(self, output):
        return all(os.path.isfile(tilepath) for tilepath in output)

    def aggregate(self, inputs, output, recipe='avg'):
        """Aggregate tiled `inputs` to files matching `output` pattern."""

        # create directory if missing
        os.makedirs(os.path.dirname(output[0]), exist_ok=True)

        # open inputs as multi-file dataset
        with xr.open_mfdataset(
                inputs, chunks={'lat': 300, 'lon': 300},
                preprocess=lambda ds: ds.assign(
                    lat=ds.lat.astype('f4'), lon=ds.lon.astype('f4')),
                ) as ds:

            # for each tile
            for tilepath, (lat, lon) in zip(output, self._get_all_coords()):

                # check wether tile file exists
                if os.path.isfile(tilepath):
                    continue

                # aggregate a 30x30 degree tile
                tile = ds.sel(lon=slice(lon, lon+30), lat=slice(lat, lat+30))
                recipe = recipe.replace('avg', 'mean')
                tile = getattr(tile, recipe)('time', keep_attrs=True)

                # store output as netcdf and return path
                print(f"aggregating {tilepath} ...")
                tile.to_netcdf(tilepath)

        # return multi-tile output pattern
        return output
