# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shaded relief plotting tools.
"""

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
            data = dataset.read(band)

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
