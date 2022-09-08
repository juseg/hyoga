# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

import numpy as np
import xarray as xr


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
    altitude = [30]*4 if altitude is None else altitude
    azimuth = [300, 315, 315, 330] if azimuth is None else azimuth

    # convert scalars to lists
    altitude = altitude if hasattr(altitude, '__iter__') else [altitude]
    azimuth = azimuth if hasattr(azimuth, '__iter__') else [azimuth]

    # check that the lists have equal lengths
    if len(altitude) != len(azimuth):
        raise ValueError("altitude and azimuth should have equal lengths")

    # compute multi-direction hillshade
    shades = sum(
        _compute_hillshade(darray, alti, azim, exag)
        for alti, azim in zip(altitude, azimuth))/len(altitude)
    return shades


def hillshade(darray, altitude=None, azimuth=None, exag=1, **kwargs):
    """Plot multidirectional hillshade image from data array.

    Parameters
    ----------
    altitude: float or iterable, optional
        Altitude angle(s) of illumination in degrees. Defaults to four light
        sources at 30 degrees. For multidirectional hillshade, ``azimuth`` and
        ``altitude`` need to have the same lenght.
    azimuth: float or iterable, optional
        Azimuth angle(s) of illumination in degrees (clockwise from north).
        Defaults to four light sources at 300, 315, 315 again and 330 azimuths.
    exag: float, optional
        Altitude exageration factor, defaults to 1.
    **kwargs: optional
        Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
        Defaults to a glossy colormap scaled linearly between -1 and 1.

    Returns
    -------
    image: AxesImage
        The plotted hillshade image.
    """
    darray = _compute_multishade(darray, altitude, azimuth, exag)
    style = dict(add_colorbar=False, cmap='Glossy', vmin=-1, vmax=1)
    style.update(**kwargs)
    return darray.plot.imshow(**style)
