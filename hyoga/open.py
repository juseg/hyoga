# Copyright (c) 2019-2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Open PISM output file as xarray datasets.
"""

import os
import re
import glob
import warnings
import numpy as np
import xarray as xr


# Private methods
# ---------------

def _preprocess(ds):
    """Prepare a newly opened dataset for convenient plotting."""

    # transpose dimensions to zyx (for older pism files)
    if 'x' in ds.dims and 'y' in ds.dims:
        ds = ds.transpose(..., 'y', 'x')

    # and assign an age dimension to a dataset with time coordinates
    if 'time' in ds.coords and 'seconds' in ds.time.units:
        ds = ds.assign_coords(age=(-ds.time/(1e3*365*24*60*60)).assign_attrs(
            long_name='model age', units='ka')).swap_dims(dict(time='age'))
    elif 'time' in ds.coords and 'years' in ds.time.units:
        ds = ds.assign_coords(age=(-ds.time/1e3).assign_attrs(
            long_name='model age', units='ka')).swap_dims(dict(time='age'))

    # return preprocessed dataset
    return ds


# Public methods
# --------------

def dataset(filename, **kwargs):
    """Open single-file dataset with age coordinate."""
    ds = xr.open_dataset(filename, decode_cf=False, **kwargs)
    ds = _preprocess(ds)
    return ds


def mfdataset(filename, **kwargs):
    """Open multi-file dataset with age coordinate."""

    # xarray expand user dir in lists but not on patterns (#4783)
    if isinstance(filename, str):
        filename = os.path.expanduser(filename)
        filelist = sorted(glob.glob(filename))
    else:
        filelist = filename

    # get global attributes from last file (attrs_file)
    # do not concatenate lon, lat etc (data_vars='minimal')
    ds = xr.open_mfdataset(
        filename, attrs_file=(filelist[-1] if filelist else None),
        data_vars='minimal', decode_cf=False, **kwargs)
    ds = _preprocess(ds)
    return ds


def subdataset(filename, time, shift=0, tolerance=1e-9, **kwargs):
    """
    Open subdataset in multi-file based on format string.

    Parameters
    ----------
    filename : str
        A format string informing the path to a series of files,
        where the unique replacement field indicate the final time in years of
        each file. For instance `path/to/ex.{:07.0f}.nc`.
    time : int of float
        Time in years (-age*1e3) used to find the file to open in the list
        matching the filename pattern, and to select a corresponding time
        slice. The format (int or float) should correspond to the format
        string used in the filename.
    shift : int or float
        Shift in years in the filename numbering relative to the model time.
        This is useful when output files are named relative to an arbitrary
        start date rather than zero.
    tolerance: float
        Largest acceptable error when selected the nearest time frame, passed
        to :meth:`xarray.Dataset.sel`.

    Returns
    -------
    ds : :class:`xarray.Dataset`
        A dataset containing the time slice defined by `time` in the multi-file
        dataset matching the `filename` pattern.
    """
    filename = os.path.expanduser(filename)
    filelist = sorted(glob.glob(re.sub('{.*}', '*', filename)))
    filename = filelist[np.searchsorted(filelist, filename.format(shift+time))]
    ds = dataset(filename, **kwargs)
    ds = ds.sel(age=-time/1e3, method='nearest', tolerance=tolerance)
    return ds


def visual(filename, bootfile, interpfile, time, ax=None, sigma=None,
           variables=None, **kwargs):
    """Open interpolated output for visualization."""
    warnings.warn(
        "open.visual() is deprecated, use open.dataset(...).interp(...) or "
        "open.subdataset(...).interp(...).", FutureWarning)
    ds = subdataset(filename, time, **kwargs)
    ds = ds.ice.visual(bootfile=bootfile, interpfile=interpfile, ax=ax,
                       sigma=sigma, variables=variables)

    # return interpolated data
    return ds
