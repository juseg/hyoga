# Copyright (c) 2019--2020, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
A thin wrapper around xarray to open PISM output files with age coordinates.
"""

import os
import re
import glob
import numpy as np
import xarray as xr
from scipy import ndimage


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


def visual(filename, bootfile, interpfile, time, sigma=None, **kwargs):
    """Open interpolated output for visualization."""
    # IDEA: would it make more sense as a dataset method?
    # pismx.open.dataset(...).visual(...)
    # pismx.open.subdataset(...).visual(...)

    # load hires bedrock topography
    with dataset(interpfile) as ds:
        hires = ds.usurf.fillna(0.0) - ds.thk.fillna(0.0)
        x = hires.x  # FIXME coords from axes
        y = hires.y  # FIXME coords from axes

    # try to smooth integer-precision steps
    if sigma is not None:
        dx = (x[-1]-x[0])/(len(x)-1)
        dy = (y[-1]-y[0])/(len(y)-1)
        assert abs(dy-dx) < 1e12
        filt = ndimage.gaussian_filter(hires, sigma=float(sigma/dx))
        hires += np.clip(filt-hires, -1.0, 1.0)

    # load boot topo
    with dataset(bootfile) as ds:
        boot = ds.topg

    # load extra data
    with subdataset(filename, time, **kwargs) as ds:
        ds = ds[['thk', 'topg', 'usurf', 'velbase_mag', 'velsurf_mag']]

        # compute ice mask and bedrock uplift
        ds['icy'] = 1.0 * (ds.thk >= 1.0)  # IDEA: return thk instead?
        ds['uplift'] = ds.topg - boot

        # interpolate surfaces to axes coords
        # FIXME custom vars besides thk, topg, usurf?
        ds = ds[['icy', 'uplift', 'usurf', 'velbase_mag', 'velsurf_mag']]
        ds = ds.interp(x=x, y=y)

    # interpolate hires topography
    ds['topg'] = hires.interp(x=x, y=y)

    # correct basal topo for uplift
    ds['topg'] = ds.topg + ds.uplift.fillna(0.0)

    # refine ice mask and pop nunataks
    ds['icy'] = (ds.icy >= 0.5) * (ds.usurf > ds.topg)
    ds['usurf'] = ds.usurf.where(ds.icy)
    ds['velsurf_mag'] = ds.velsurf_mag.where(ds.icy)

    # return interpolated data
    return ds
