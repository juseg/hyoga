# Copyright (c) 2019--2020, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Topographic profile tools.
"""

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.io.shapereader as cshp


def build_profile_coords(points, interval=None, method='linear'):
    """Interpolate coordinates along profile through given points."""

    # compute distance along profile
    x, y = np.asarray(points).T
    dist = ((np.diff(x)**2+np.diff(y)**2)**0.5).cumsum()
    dist = np.insert(dist, 0, 0)

    # build coordinate xarrays
    x = xr.DataArray(x, coords=[dist], dims='d')
    y = xr.DataArray(y, coords=[dist], dims='d')

    # if interval was given, interpolate coordinates
    if interval is not None:
        dist = np.arange(0, dist[-1], interval)
        x = x.interp(d=dist, method=method)
        y = y.interp(d=dist, method=method)

    # return coordinates
    return x, y


def read_shp_coords(filename, crs=None, **kwargs):
    """Read and interpolate coordinates along profile from shapefile."""

    # read profile from shapefile
    shp = cshp.Reader(filename)
    geom = next(shp.geometries())
    points = np.asarray(geom)
    if crs is not None:
        points = crs.transform_points(ccrs.PlateCarree(), *points.T)[:, :2]
    x, y = build_profile_coords(points, **kwargs)

    # return coordinates
    return x, y
