# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

import numpy as np
import rasterio
import rasterio.mask
import matplotlib.pyplot as plt
import cartopy.io.shapereader as cshp
import cartowik.conventions as ccv


# Shaded relief internals
# -----------------------

def _open_raster_data(filename, band=1, mask=None, offset=0.0):
    """Open raster and return data and extent."""

    # open raster data
    with rasterio.open(filename) as dataset:
        bounds = dataset.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # extract raw data
        if mask is None:
            data = dataset.read(band, masked=True)

        # extract data with land mask
        elif mask == 'land':
            shapefile = cshp.Reader(cshp.natural_earth(
                resolution='10m', category='physical', name='land'))
            shapes = list(shapefile.geometries())
            data, _ = rasterio.mask.mask(
                dataset, shapes, indexes=band, filled=False)

    # apply offset
    data = data - offset

    # return data and extent
    return data, extent


def _compute_hillshade(data, extent, altitude=30.0, azimuth=315.0, exag=1.0):
    """Compute transparent hillshade map from a data array and extent."""

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
    xres = (extent[1]-extent[0])/data.shape[1]
    yres = (extent[3]-extent[2])/data.shape[0]
    grady, gradx = np.gradient(exag*data, xres, yres)

    # compute hillshade (minus dot product of normal and light direction)
    shades = (gradx*lsx + grady*lsy - lsz) / (1 + gradx**2 + grady**2)**(0.5)
    return shades


# Shaded relief plotting
# ----------------------

def add_bathymetry(filename, ax=None, mask=None, offset=0.0):
    """Add bathymetric image from raster file."""

    # get current axes if None provided
    ax = ax or plt.gca()

    # open bathymetric data
    data, extent = _open_raster_data(filename, mask=mask, offset=offset)

    # plot bathymetry
    ax.imshow(data, cmap=ccv.COLORMAPS['Bathymetric'], extent=extent,
              interpolation='bilinear', origin='upper',
              transform=ax.projection, vmin=-6000, vmax=0)


def add_topography(filename, ax=None, mask=None, offset=0.0):
    """Add topographic image from raster file."""

    # get current axes if None provided
    ax = ax or plt.gca()

    # open topographic data
    data, extent = _open_raster_data(filename, mask=mask, offset=offset)

    # plot topography
    ax.imshow(data, cmap=ccv.COLORMAPS['Topographic'], extent=extent,
              interpolation='bilinear', origin='upper',
              transform=ax.projection, vmin=0, vmax=9000)


def add_hillshade(filename, ax=None, mask=None, offset=0.0, azimuth=315.0,
                  altitude=30.0, exag=1.0):
    """Add hillshades image from raster file."""

    # get current axes if None provided
    ax = ax or plt.gca()

    # open topographic data and compute hillshades
    data, extent = _open_raster_data(filename, mask=mask, offset=offset)
    shades = _compute_hillshade(data, extent, altitude=altitude,
                                azimuth=azimuth, exag=exag)

    # plot shading
    ax.imshow(shades, cmap=ccv.COLORMAPS['Shines'], extent=extent,
              interpolation='bilinear', origin='upper', vmin=-1.0, vmax=1.0)
