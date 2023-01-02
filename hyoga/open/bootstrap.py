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


def bootstrap(crs, extent, resolution=1e3):
    """
    Open bootstrapping data from online datasets for PISM.

    Currently a single dataset (GEBCO) is supported.

    Parameters
    ----------
    crs : str
        Coordinate reference system for the resulting dataset as OGC WKT or
        Proj.4 string, will be passed to Dataset.rio.reproject.
    extent : (west, east, south, north)
        Extent for the resulting dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.clip_box.
    resolution : float, optional
        Resolution for the output dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.reproject.

    Returns
    -------
    ds : Dataset
        The resulting dataset containing surface variables with the requested
        ``crs``, ``extent``, and ``resolution``. Use ``ds.to_netcdf()`` to
        export as PISM bootstrapping file.
    """

    # open global data (use decode_coords='all' to read grid_mapping attribute)
    filepath = _download_gebco()
    ds = xr.open_dataset(filepath, decode_coords='all')

    # clip, reproject and clip again
    west, east, south, north = extent
    ds = ds.rio.clip_box(west, south, east, north, crs=crs)
    ds = ds.rio.reproject(crs, resolution=resolution)
    ds = ds.rio.clip_box(west, south, east, north)

    # flip data to increasing y-coord (needed by PISM)
    ds = ds.isel(y=slice(None, None, -1))

    # set better standard name
    ds.elevation.attrs.update(standard_name='bedrock_altitude')

    # return projected dataset
    return ds
