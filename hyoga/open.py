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
    # NOTE this will be moved to hyoga.hyoga in the future
    # NOTE code will be more robust if using decode_cf=True

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
    """Open a single-file model output dataset.

    Parameters
    ----------
    filename : str, Path, file-like or DataStore
        Path to a model input or output file containing the data to open.
        Variables should in principle contain a ``'standard_name'`` attribute
        following the Climate and Forecast conventions. Some standard names
        will be filled according to PISM variable short names if missing.
        This mechanism is not yet implemented for other models.
    **kwargs : optional
        Keyword arguments passed :func:`xarray.open_dataset`.

    Returns
    -------
    ds : Dataset
        Xarray dataset containing variables in the file.
    """
    kwargs.setdefault('decode_cf', False)  # NOTE needed by current age code
    ds = xr.open_dataset(filename, **kwargs)
    ds = _preprocess(ds)
    return ds


def mfdataset(filename, **kwargs):
    """Open a multi-file model output dataset.

    Parameters
    ----------
    filename : str or sequence
        Either a string containing wildcards (``'path/to/*.nc'``) or an
        explicit list of files to open (see :func:`xarray.open_mfdataset`).
    **kwargs : optional
        Keyword arguments passed :func:`xarray.open_mfdataset`. By default
        global attributes will be read from the last file (preserving history
        from a series of runs) and a ``'minimal'`` set of data variables (not
        including lon, lat, etc) will be concatenated across files.

    Returns
    -------
    ds : Dataset
        Xarray dataset containing variables in the files.
    """

    # xarray expand user dir in lists but not on patterns (#4783)
    if isinstance(filename, str):
        filename = os.path.expanduser(filename)
        filelist = sorted(glob.glob(filename))
    else:
        filelist = filename

    # get global attributes from last file (attrs_file)
    # do not concatenate lon, lat etc (data_vars='minimal')
    options = dict(
        attrs_file=(filelist[-1] if filelist else None),
        data_vars='minimal', decode_cf=False)
    options.update(**kwargs)
    ds = xr.open_mfdataset(filename, **options)
    ds = _preprocess(ds)
    return ds


def subdataset(filename, time, shift=0, tolerance=1e-9, **kwargs):
    """
    Open a single file in a multi-file dataset.

    Parameters
    ----------
    filename : str
        A format string informing the path to a series of files. A single
        replacement field should indicate the final time in years of each file
        (e.g. ``'path/to/ex.{:07.0f}.nc'``).
    time : int of float
        Time in years (-age*1e3) used to find the file to open in the list
        matching the filename pattern, and to select a corresponding time
        slice. The format (int or float) should correspond to the format
        string used in the filename.
    shift : int or float
        Shift in years in the filename numbering relative to the model time.
        This is useful when output files are named relative to an arbitrary
        start date rather than zero, for instance in paleo-glacier runs.
    tolerance: float
        Largest acceptable error when selected the nearest time frame, passed
        to :meth:`xarray.Dataset.sel`.
    **kwargs : optional
        Keyword arguments passed :func:`dataset`.

    Returns
    -------
    ds : Dataset
        Dataset containing the time slice defined by ``time`` in the multi-file
        dataset matching the ``filename`` pattern.
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
    return ds
