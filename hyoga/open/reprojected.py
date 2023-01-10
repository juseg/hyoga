# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contain function to open reprojected raster from online sources
stored in the hyoga cache directory. The resulting datasets can be exported as
PISM input files (bootstrapping and atmosphere files) using `ds.to_netcdf()`.
Geographic reprojection is handled by rioxarray.
"""

import affine
import numpy as np
import xarray as xr
import rioxarray  # noqa pylint: disable=unused-import

import hyoga.open.downloader


def _open_elevation(source='gebco'):
    """Open elevation data (bedrock or surface) from online source."""

    # GEBCO global elevation data
    if source == 'gebco':
        downloader = hyoga.open.downloader.ZipDownloader()
        path = downloader(
            'https://www.bodc.ac.uk/data/open_download/gebco/'
            'gebco_2022_sub_ice_topo/zip/', 'gebco/GEBCO_2022_sub_ice_topo.nc')
        da = xr.open_dataarray(path, decode_coords='all', decode_cf=True)

    # CHELSA climate data input DEM
    elif source == 'chelsa':
        downloader = hyoga.open.downloader.CacheDownloader()
        path = downloader(
            'https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V2/'
            'GLOBAL/input/dem_latlong.nc', 'chelsa/dem_latlong.nc')
        da = xr.open_dataarray(path, decode_coords='all')
        da = da.isel(lat=slice(None, None, -1))

    # invalid sources
    else:
        raise ValueError(f'{source} is not a valid elevation data source.')

    # return selected data array
    return da


def _open_climatology(source='chelsa', variable='tas'):
    """Open monthly climatology (temperature or precip) from online source."""

    # CHELSA 1981-2010 global climatologies
    if source == 'chelsa':
        downloader = hyoga.open.downloader.CacheDownloader()
        basenames = (
            f'CHELSA_{variable}_{month+1:02d}_1981-2010_V.2.1.tif'
            for month in range(12))
        paths = (downloader(
            'https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V2/'
            f'GLOBAL/climatologies/1981-2010/{variable}/{basename}',
            f'chelsa/{basename}') for basename in basenames)
        ds = xr.open_mfdataset(
            paths, combine='nested', concat_dim='time', decode_cf=True)
        da = ds.band_data.squeeze()

    # invalid sources
    else:
        raise ValueError(f'{source} is not a valid climatology source.')

    # return selected data array
    return da


def _reproject_data_array(da, crs, extent, resolution):
    """Reproject data array to exact bounds via affine transform."""
    west, east, south, north = extent
    da = da.rio.clip_box(west, south, east, north, crs=crs)
    bounds = da.rio.transform_bounds(crs)
    xoffset = bounds[0] - bounds[0] % resolution
    yoffset = bounds[1] - bounds[1] % resolution
    transform = affine.Affine(resolution, 0, xoffset, 0, resolution, yoffset)
    da = da.rio.reproject(crs, transform=transform, resampling=1)
    da = da.rio.clip_box(west, south, east, north)
    return da


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

    # open reprojected elevation data
    da = _open_elevation(source='gebco')
    da = _reproject_data_array(da, crs, extent, resolution)

    # set better standard name
    da.attrs.update(standard_name='bedrock_altitude')

    # return as dataset
    return da.to_dataset()
