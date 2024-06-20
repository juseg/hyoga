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

    def check(self, path):
        """Check whether output file is present."""
        return os.path.isfile(path)

    def aggregate(self, inputs, output, recipe='avg'):
        """Aggregate `inputs` into `output` file."""

        # create directory if missing
        os.makedirs(os.path.dirname(output), exist_ok=True)

        # open inputs as multi-file dataset
        with xr.open_mfdataset(
                inputs, chunks={'lat': 300, 'lon': 300},
                # FIXME this is a mixed-precision workaround specific to CW5E5
                preprocess=lambda ds: ds.assign(
                    lat=ds.lat.astype('f4'), lon=ds.lon.astype('f4'))) as ds:
            ds = getattr(
                ds, recipe.replace('avg', 'mean'))('time', keep_attrs=True)

            # store output as netcdf and return path
            print(f"aggregating {output} ...")
            ds.to_netcdf(output)
            return output


class CW5E5ClimateAggregator(Aggregator):
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

    def inputs(self, *args):
        """Return paths of input files, downloading as necessary."""
        variable, start, end, month = args
        downloader = hyoga.open.downloader.CW5E5DailyDownloader()
        years = range(start, end+1)
        paths = (downloader(variable, year, month) for year in years)
        return paths

    def output(self, *args):
        """Return path of downloaded file."""
        variable, start, end, month = args
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(
            os.path.expanduser('~'), '.cache'))
        return os.path.join(
            xdg_cache, 'hyoga', 'cw5e5', 'clim', f'cw5e5.{variable}.mon.'
            f'{start % 100:02d}{end % 100:02d}.avg.{month:02d}.nc')
