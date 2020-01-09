# Copyright (c) 2019--2020, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A thin wrapper around xarray to open PISM output files with age coordinates.
"""

import os
import glob
import xarray as xr


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
    filename = os.path.expanduser(filename)
    # get global attributes from last file (issue #2382 fixed in juseg/xarray)
    # do not concatenate lon, lat etc (data_vars='minimal')
    ds = xr.open_mfdataset(
        filename, attrs_file=sorted(glob.glob(filename))[-1],
        combine='by_coords', data_vars='minimal', decode_cf=False, **kwargs)
    ds = _assign_age_dim(ds)
    return ds
