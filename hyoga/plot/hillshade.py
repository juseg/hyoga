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


def _compute_hillshade(darray, altitude=30.0, azimuth=315.0):
    """Compute transparent hillshade map from a data array."""
    # IDEA: try using higher-order differences to smooth the result

    # convert to rad
    azimuth *= np.pi / 180.
    altitude *= np.pi / 180.

    # compute cartesian coords of the illumination direction
    lsx = np.sin(azimuth) * np.cos(altitude)
    lsy = np.cos(azimuth) * np.cos(altitude)
    lsz = np.sin(altitude)

    # compute topographic gradient
    grady, gradx = _compute_gradient(darray)

    # compute hillshade (minus dot product of normal and light direction)
    shades = (gradx*lsx + grady*lsy - lsz) / (1 + gradx**2 + grady**2)**(0.5)

    # set horizontal surfaces hillshade to zero
    # NOTE: would it make sense to remap this to (-1, 1)?
    # - in theory shades go from -1 to +1 (orthogonal surfaces)
    # - in practice they go from -1 to cos(altitude) (a vertical surface)
    # - currently we remap [-1; cos(a)] to [sin(a)-1; cos(a)-sin(a)]
    # - therefore we leave vmin and vmax unspecified in hillshade() below.
    shades = shades + lsz

    # return hillshade array
    return shades


def _compute_multishade(darray, altitude=None, azimuth=None, weight=None):
    """Compute multi-direction hillshade map from a data array."""

    # default light source parameters
    altitude = 45 if altitude is None else altitude
    azimuth = [255, 315, 15] if azimuth is None else azimuth
    weight = [0.25, 0.5, 0.25] if weight is None else weight

    # find arguments provided as iterables
    kwargs = dict(altitude=altitude, azimuth=azimuth, weight=weight)
    iterargs = {k: v for k, v in kwargs.items() if hasattr(v, '__iter__')}

    # ensure they have equal length (default lenght to 1)
    length = len(list(iterargs.values())[0]) if iterargs else 1
    if not all(len(arg) == length for arg in iterargs.values()):
        raise ValueError("iterable arguments should have equal lengths")

    # convert scalars to lists
    altitude = iterargs.get('altitude', [altitude]*length)
    azimuth = iterargs.get('azimuth', [azimuth]*length)
    weight = iterargs.get('weight', [weight]*length)

    # compute multi-direction hillshade
    shades = sum(
        _compute_hillshade(darray, alti, azim)*wgt
        for alti, azim, wgt in zip(altitude, azimuth, weight))
    return shades


def hillshade(darray, altitude=None, azimuth=None, weight=None, **kwargs):
    """Plot multidirectional hillshade image from data array.

    Parameters
    ----------
    altitude: float or iterable, optional
        Altitude angle(s) of illumination in degrees. Defaults to three light
        sources at 45 degrees. Any of ``azimuth``, ``altitude`` and ``weight``
        provided as iterables need to have equal lengths.
    azimuth: float or iterable, optional
        Azimuth angle(s) of illumination in degrees (clockwise from north).
        Defaults to three light sources at 255, 315 and 15 degree azimuths.
    weight: float or iterable, optional
        Weight coefficient(s) for each unidirectional hillshade array. It is
        intended, but not required, that the weights add up to 1.
        Defaults to [0.25, 0.5, 0.25].
    **kwargs: optional
        Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
        Defaults to a glossy colormap scaled linearly between -1 and 1.

    Returns
    -------
    image: AxesImage
        The plotted hillshade image.
    """
    darray = _compute_multishade(darray, altitude, azimuth, weight)
    style = dict(add_colorbar=False, cmap='Glossy')
    style.update(**kwargs)
    return darray.plot.imshow(**style)
