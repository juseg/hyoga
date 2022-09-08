# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

import numpy as np
import xarray as xr


# Shaded relief internals
# -----------------------

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
    # for transparent shades set horizontal surfaces to zero
    lsx = np.sin(azimuth) * np.cos(altitude)
    lsy = np.cos(azimuth) * np.cos(altitude)
    lsz = 0.0  # (0.0 if transparent else np.sin(altitude))

    # compute topographic gradient
    grady, gradx = _compute_gradient(exag*darray)

    # compute hillshade (minus dot product of normal and light direction)
    shades = (gradx*lsx + grady*lsy - lsz) / (1 + gradx**2 + grady**2)**(0.5)
    return shades


def _compute_multishade(darray, altitude=None, azimuth=None, exag=1.0):
    """Compute multi-direction hillshade map from a data array."""

    # default light source parameters
    # FIXME this will also overwrite altitude=0
    altitude = altitude or [30.0]*4
    azimuth = azimuth or [300.0, 315.0, 315.0, 330.0]

    # convert scalars to lists
    altitude = altitude if hasattr(altitude, '__iter__') else [altitude]
    azimuth = azimuth if hasattr(azimuth, '__iter__') else [azimuth]

    # check that the lists have equal lengths
    if len(altitude) != len(azimuth):
        raise ValueError("altitude and azimuth should have equal lengths")

    # compute multi-direction hillshade
    shades = sum([_compute_hillshade(darray, alti, azim, exag)
                  for alti, azim in zip(altitude, azimuth)])/len(altitude)
    return shades


def _add_imshow(darray, add_colorbar=False, add_labels=False, cmap=None,
                interpolation='bilinear', **kwargs):
    """Wrapper for imshow enabling custom conventions and defaults."""
    # cmap = ccv.COLORMAPS.get(cmap, cmap)  # no longer needed
    return darray.plot.imshow(add_colorbar=add_colorbar, add_labels=add_labels,
                              cmap=cmap, interpolation=interpolation, **kwargs)


# Shaded relief plotting
# ----------------------

def add_hillshade(darray,
                  altitude=30.0, azimuth=315.0, exag=1.0,
                  cmap='Glossy', vmin=-1.0, vmax=1.0, **kwargs):
    """Add hillshades image from raster file."""

    # open topographic data and compute hillshades
    darray = _compute_hillshade(darray, altitude, azimuth, exag)

    # plot shading
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def hillshade(darray, altitude=None, azimuth=None, exag=1, **kwargs):
    """Add multi-direction hillshade image from raster file."""
    darray = _compute_multishade(darray, altitude, azimuth, exag)
    style = dict(add_colorbar=False, cmap='Glossy', vmin=-1, vmax=1)
    style.update(**kwargs)
    return darray.plot.imshow(**style)
