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


def _coords_from_axes(ax):
    """Compute coordinate vectors from matplotlib axes."""
    bbox = ax.get_window_extent()
    return _coords_from_extent(
        ax.get_extent(), int(round(bbox.width)), int(round(bbox.height)))


def _coords_from_extent(extent, cols, rows):
    """Compute coordinate vectors from image extent."""

    # compute dx and dy
    (west, east, south, north) = extent
    dx = (east-west) / cols
    dy = (north-south) / rows

    # prepare coordinate vectors
    xwcol = west + 0.5*dx  # x-coord of W row cell centers
    ysrow = south + 0.5*dy  # y-coord of N row cell centers
    x = xwcol + np.arange(cols)*dx  # from W to E
    y = ysrow + np.arange(rows)*dy  # from S to N

    # return coordinate vectors
    return x, y


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


def subdataset(filename, time, shift=0, **kwargs):
    """Open subdataset in multi-file based on format string."""
    filename = os.path.expanduser(filename)
    filelist = sorted(glob.glob(re.sub('{.*}', '*', filename)))
    filename = filelist[np.searchsorted(filelist, filename.format(shift+time))]
    ds = dataset(filename, **kwargs)
    ds = ds.sel(age=-time/1e3, method='nearest', tolerance=1e-12)
    return ds


def visual(filename, bootfile, interpfile, time, ax=None, sigma=None,
           **kwargs):
    """Open interpolated output for visualization."""
    # IDEA: would it make more sense as a dataset method?
    # the way to go about this apparently is through accessors
    # http://xarray.pydata.org/en/stable/internals.html#extending-xarray
    # pismx.open.dataset(...).px.visual(...)
    # pismx.open.subdataset(...).px.visual(...)

    # load hires bedrock topography
    with dataset(interpfile) as ds:
        hires = ds.usurf.fillna(0.0) - ds.thk.fillna(0.0)

    # interpolation coordinates
    if ax is not None:
        x, y = _coords_from_axes(ax)
    else:
        x = hires.x
        y = hires.y

    # try to smooth integer-precision steps
    # IDEA: can we avoid scipy.ndimage?
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

        # compute ice mask and bedrock uplift
        ds['icy'] = 1.0 * (ds.thk >= 1.0)
        ds['uplift'] = ds.topg - boot

        # interpolate surfaces to axes coords
        # FIXME custom vars besides thk, topg, usurf?
        ds = ds[['icy', 'thk', 'uplift', 'usurf', 'velbase_mag', 'velsurf_mag']]
        ds = ds.interp(x=x, y=y)

    # interpolate hires topography
    ds['topg'] = hires.interp(x=x, y=y)

    # correct basal topo for uplift
    ds['topg'] = ds.topg + ds.uplift.fillna(0.0)

    # refine ice mask and pop nunataks
    ds['icy'] = ds.icy * (ds.usurf > ds.topg)
    ds['thk'] = ds.thk.where(ds.icy)
    ds['usurf'] = ds.usurf.where(ds.icy)
    ds['velbase_mag'] = ds.velbase_mag.where(ds.icy)
    ds['velsurf_mag'] = ds.velsurf_mag.where(ds.icy)

    # return interpolated data
    return ds
