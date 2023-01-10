# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contain function to open reprojected raster from online sources
stored in the hyoga cache directory. The resulting datasets can be exported as
PISM input files (bootstrapping and atmosphere files) using `ds.to_netcdf()`.
Geographic reprojection is handled by rioxarray.
"""

import affine
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

    # open global data (use decode_coords='all' to read grid_mapping attribute)
    filepath = _download_gebco()
    da = xr.open_dataarray(filepath, decode_coords='all', decode_cf=True)

    # reproject to match bounds
    da = _reproject_data_array(da, crs, extent, resolution)

    # set better standard name
    da.attrs.update(standard_name='bedrock_altitude')

    # return as dataset
    return da.to_dataset()
