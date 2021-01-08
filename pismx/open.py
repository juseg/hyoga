# Copyright (c) 2019--2020, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A thin wrapper around xarray to open PISM output files with age coordinates.
"""

import os
import re
import glob
import xarray as xr
import numpy as np


def _assign_age_dim(ds):
    """Assign age dimension to a dataset with time coordinates."""
    if 'time' in ds.coords and 'seconds' in ds.time.units:
        ds = ds.assign_coords(age=(-ds.time/(1e3*365*24*60*60)).assign_attrs(
            long_name='model age', units='ka')).swap_dims(dict(time='age'))
    elif 'time' in ds.coords and 'years' in ds.time.units:
        ds = ds.assign_coords(age=(-ds.time/1e3).assign_attrs(
            long_name='model age', units='ka')).swap_dims(dict(time='age'))
    return ds


def dataset(filename, **kwargs):
    """Open single-file dataset with age coordinate."""
    ds = xr.open_dataset(filename, decode_cf=False, **kwargs)
    ds = _assign_age_dim(ds)
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
    ds = _assign_age_dim(ds)
    return ds


def subdataset(filename, time, shift=0, **kwargs):
    """Open subdataset in multi-file based on format string."""
    filename = os.path.expanduser(filename)
    filelist = sorted(glob.glob(re.sub('{.*}', '*', filename)))
    filename = filelist[np.searchsorted(filelist, filename.format(shift+time))]
    ds = dataset(filename, **kwargs)
    ds = ds.sel(age=-time/1e3, method='nearest', tolerance=1e-12)
    return ds
