# Copyright (c) 2018, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

import numpy as np
import xarray as xr
import cartowik.conventions as ccv


# Shaded relief internals
# -----------------------

def _open_data_source(datasource, mask=None, offset=0):
    """
    Open data source and return data array needed for plotting.

    Parameters
    ----------
    datasource: string
        A data array or the path to a data file to be opened with rasterio.
    mask: None
        Not implemented yet.
    offset: scalar, optional
        Substract this number to the data. Mostly used to fix data stored as
        unsigned integers.
    """
    if isinstance(datasource, xr.DataArray):
        darray = datasource
    else:
        darray = xr.open_rasterio(datasource)
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
    # for transparent shades set horizontal surfaces to zero
    lsx = np.sin(azimuth) * np.cos(altitude)
    lsy = np.cos(azimuth) * np.cos(altitude)
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


def _add_contours(darray, add_colorbar=False, add_labels=False, cmap=None,
                  colors=None, levels=None, **kwargs):
    """Wrapper for contourf enabling custom conventions and defaults."""

    # for registed Cartowik colormaps
    if cmap in ccv.CLISTS and cmap in ccv.LEVELS:

        # replace colormap by color list and levels
        colors = colors or ccv.CLISTS.get(cmap, None)
        colors = colors + [colors[-1]]
        levels = levels or ccv.LEVELS.get(cmap, None)
        cmap = None

        # normalize levels if vmin or vmax are provided
        lmin = levels[0]
        lmax = levels[-1]
        vmin = kwargs.pop('vmin', lmin)
        vmax = kwargs.pop('vmax', lmax)
        levels = [vmin+(vmax-vmin)*(l-lmin)/(lmax-lmin) for l in levels]

        # providing darray.plot.contourf with a BoundaryNorm results in the
        # colormap to be reset, so the following code does not work:
        # import matplotlib as mpl
        # cmap, norm = mpl.colors.from_levels_and_colors(
        #     levels, colors, extend='both')

    # so we pass colors and levels directly but we need to enforce
    # extend='both' for accurate color mapping (esp. depressions)
    return darray.plot.contourf(
        add_colorbar=add_colorbar, add_labels=add_labels, colors=colors,
        levels=levels, extend='both', **kwargs)


def _add_imshow(darray, add_colorbar=False, add_labels=False, cmap=None,
                interpolation='bilinear', **kwargs):
    """Wrapper for imshow enabling custom conventions and defaults."""
    cmap = ccv.COLORMAPS.get(cmap, cmap)
    return darray.plot.imshow(add_colorbar=add_colorbar, add_labels=add_labels,
                              cmap=cmap, interpolation=interpolation, **kwargs)


# Shaded relief plotting
# ----------------------

def add_bathymetry(datasource, mask=None, offset=0.0,
                   cmap='Bathymetric', vmin=-6000, vmax=0, **kwargs):
    """Add bathymetric image from raster file."""

    # open bathymetric data
    darray = _open_data_source(datasource, mask=mask, offset=offset)

    # plot bathymetry
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_bathymetry_contours(datasource, mask=None, offset=0.0,
                            cmap='Bathymetric', vmin=-6000, vmax=0, **kwargs):
    """Add bathymetric contours from raster file."""

    # open topographic data
    darray = _open_data_source(datasource, mask=mask, offset=offset)

    # plot topography
    return _add_contours(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_topography(datasource, mask=None, offset=0.0,
                   cmap='Topographic', vmin=0, vmax=9000, **kwargs):
    """Add topographic image from raster file."""

    # open topographic data
    darray = _open_data_source(datasource, mask=mask, offset=offset)

    # plot topography
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_topography_contours(datasource, mask=None, offset=0.0,
                            cmap='Topographic', vmin=0, vmax=9000, **kwargs):
    """Add topographic contours from raster file."""

    # open topographic data
    darray = _open_data_source(datasource, mask=mask, offset=offset)

    # plot topography
    return _add_contours(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_hillshade(datasource, mask=None, offset=0.0,
                  altitude=30.0, azimuth=315.0, exag=1.0,
                  cmap='Shines', vmin=-1.0, vmax=1.0, **kwargs):
    """Add hillshades image from raster file."""

    # open topographic data and compute hillshades
    darray = _open_data_source(datasource, mask=mask, offset=offset)
    darray = _compute_hillshade(darray, altitude, azimuth, exag)

    # plot shading
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)


def add_multishade(datasource, mask=None, offset=0.0,
                   altitudes=None, azimuths=None, exag=1.0,
                   cmap='Shines', vmin=-1.0, vmax=1.0, **kwargs):
    """Add multi-direction hillshade image from raster file."""

    # open topographic data and compute hillshades
    darray = _open_data_source(datasource, mask=mask, offset=offset)
    darray = _compute_multishade(darray, altitudes, azimuths, exag)

    # plot hillshades
    return _add_imshow(darray, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
