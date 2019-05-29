# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

import numpy as np
import xarray as xr
import cartowik.conventions as ccv


# Shaded relief internals
# -----------------------

def _open_raster_data(filename, mask=None, offset=0):
    """
    Open raster file and return data array.

    Parameters
    ----------
    filename: string
        Path to data file in any format supported by rasterio.
    mask: None
        Not implemented yet.
    offset: scalar, optional
        Substract this number to the data. Mostly used to fix data stored as
        unsigned integers.
    """
    darray = xr.open_rasterio(filename)
    darray = darray.where(~darray.isin(darray.nodatavals))
    darray = darray.squeeze() - offset
    return darray


def _compute_gradient(darray):
    """Compute gradient along a all dimensions of a data array."""

    # extract coordinate data
    dims = darray.dims
    coords = [darray[d].data for d in dims]

    # apply numpy.gradient
    darray = xr.apply_ufunc(np.gradient, darray, *coords,
                            input_core_dims=(dims,)+dims,
                            output_core_dims=[('n',)+dims])

    # add vector component coordinate
    darray = darray.assign_coords(n=list(dims))

    # return as single dataarray
    return darray


def _compute_hillshade(darray, altitude=30.0, azimuth=315.0, exag=1.0):
    """Compute transparent hillshade map from a data array."""

    # convert to rad
    azimuth *= np.pi / 180.
    altitude *= np.pi / 180.

    # compute cartesian coords of the illumination direction
    # rasterio's y-axis is inverted from north to south
    # for transparent shades set horizontal surfaces to zero
    lsx = np.sin(azimuth) * np.cos(altitude)
    lsy = -np.cos(azimuth) * np.cos(altitude)
    lsz = 0.0  # (0.0 if transparent else np.sin(altitude))

    # compute topographic gradient
    grady, gradx = _compute_gradient(exag*darray)

    # compute hillshade (minus dot product of normal and light direction)
    shades = (gradx*lsx + grady*lsy - lsz) / (1 + gradx**2 + grady**2)**(0.5)
    return shades


def _compute_multishade(darray, altitudes=None, azimuths=None, exag=1.0):
    """Compute multi-direction hillshade map from a data array."""

    # default light source parameters
    altitudes = altitudes or [30.0]*4
    azimuths = azimuths or [300.0, 315.0, 315.0, 330.0]

    # check that the lists have equal lengths
    if len(altitudes) != len(azimuths):
        raise ValueError("altitudes and azimuths should have equal lengths")

    # compute multi-direction hillshade
    shades = sum([_compute_hillshade(darray, alti, azim, exag)
                  for alti, azim in zip(altitudes, azimuths)])/len(altitudes)
    return shades


def _add_imshow(darray, cmap=None, interpolation='bilinear', **kwargs):
    """Wrapper for imshow enabling custom conventions and defaults."""
    cmap = ccv.COLORMAPS.get(cmap, cmap)
    return darray.plot.imshow(add_colorbar=False, add_labels=False, cmap=cmap,
                              interpolation=interpolation, **kwargs)


# Shaded relief plotting
# ----------------------

def add_bathymetry(filename, mask=None, offset=0.0,
                   cmap='Bathymetric', vmin=-6000, vmax=0, **kwargs):
    """Add bathymetric image from raster file."""

    # open bathymetric data
    darray = _open_raster_data(filename, mask=mask, offset=offset)

    # plot bathymetry
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_topography(filename, mask=None, offset=0.0,
                   cmap='Topographic', vmin=0, vmax=9000, **kwargs):
    """Add topographic image from raster file."""

    # open topographic data
    darray = _open_raster_data(filename, mask=mask, offset=offset)

    # plot topography
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_hillshade(filename, mask=None, offset=0.0,
                  altitude=30.0, azimuth=315.0, exag=1.0,
                  cmap='Shines', vmin=-1.0, vmax=1.0, **kwargs):
    """Add hillshades image from raster file."""

    # open topographic data and compute hillshades
    darray = _open_raster_data(filename, mask=mask, offset=offset)
    darray = _compute_hillshade(darray, altitude, azimuth, exag)

    # plot shading
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_multishade(filename, mask=None, offset=0.0,
                   altitudes=None, azimuths=None, exag=1.0,
                   cmap='Shines', vmin=-1.0, vmax=1.0, **kwargs):
    """Add multi-direction hillshade image from raster file."""

    # open topographic data and compute hillshades
    darray = _open_raster_data(filename, mask=mask, offset=offset)
    darray = _compute_multishade(darray, altitudes, azimuths, exag)

    # plot hillshades
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
