# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a function to open surface-level bootstrapping datasets
for predefined domains, including altitude, ice thickness and geothermal heat
flux data.
"""

import xarray as xr
import rioxarray  # noqa pylint: disable=unused-import

import hyoga.open.downloader


def _download_gebco():
    """Download GEBCO sub-ice bathymetric and topographic data."""
    downloader = hyoga.open.downloader.ZipDownloader()
    filepath = downloader(
        'https://www.bodc.ac.uk/data/open_download/gebco/'
        'gebco_2022_sub_ice_topo/zip/', 'gebco/GEBCO_2022_sub_ice_topo.nc')
    return filepath


def surface(crs, extent, resolution=1e3):
    """Open online surface data."""

    # open global data
    filepath = _download_gebco()
    ds = xr.open_dataset(filepath)
    ds = ds.rio.write_crs(ds.crs.epsg_code)

    # clip, reproject and clip again
    west, east, south, north = extent
    ds = ds.rio.clip_box(west, south, east, north, crs=crs)
    ds = ds.rio.reproject(crs, resolution=resolution)
    ds = ds.rio.clip_box(west, south, east, north)

    # set better standard name
    ds.elevation.attrs.update(standard_name='bedrock_altitude')

    # return projected dataset
    return ds
