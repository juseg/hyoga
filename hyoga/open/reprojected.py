# Copyright (c) 2022-2025, Julien Seguinot (juseg.dev)
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

import hyoga.open.aggregator
import hyoga.open.downloader


def _clear_scaling_attributes(ds):
    """Clear scaled encoding attributes not understood by PISM."""
    for var in ds.data_vars.values():
        var.encoding.pop('add_offset', None)
        var.encoding.pop('scale_factor', None)
        var.encoding.pop('dtype', None)


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
            'https://os.zhdk.cloud.switch.ch/chelsav2/'
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
            'https://os.zhdk.cloud.switch.ch/chelsav2/'
            f'GLOBAL/climatologies/1981-2010/{variable}/{basename}',
            f'chelsa/{basename}') for basename in basenames)
        ds = xr.open_mfdataset(
            paths, combine='nested', concat_dim='time', decode_cf=True)
        da = ds.band_data.squeeze()

    # CHELSA 1981-2010 global climatologies
    elif source == 'cw5e5':
        aggregator = hyoga.open.aggregator.CW5E5TiledAggregator()
        start, end = 1981, 2010  # FIXME allow custom aggregation period
        paths = aggregator(variable, start, end)
        ds = xr.open_mfdataset(paths, decode_cf=True)
        ds = ds.rename_dims(month='time')  # FIXME move to aggregator?
        da = ds[variable].rio.write_crs('+proj=longlat +datum=WGS84')

    # invalid sources
    else:
        raise ValueError(f'{source} is not a valid climatology source.')

    # return selected data array
    return da


def _reproject_data_array(da, crs, bounds, resolution):
    """Reproject data array to exact bounds via affine transform."""

    # clip around target bounds
    da = da.rio.clip_box(crs=crs, *bounds)

    # compute affine transform
    west, south, east, north = bounds
    transform = affine.Affine(resolution, 0, west, 0, resolution, south)

    # compute output shape
    cols = int((east-west)/resolution)
    rows = int((north-south)/resolution)
    shape = (rows, cols)

    # reproject to new crs
    da = da.rio.reproject(crs, transform=transform, resampling=1, shape=shape)

    # rename grid_mapping to avoid different values in datasets (#72)
    da = da.rename({da.encoding['grid_mapping']: 'spatial_ref'})
    da.encoding.update(grid_mapping='spatial_ref')

    # return reprojected data
    return da


def atmosphere(
        crs, bounds, temperature='chelsa', precipitation=None, resolution=1e3):
    """
    Open atmospheric data from online datasets for PISM.

    Parameters
    ----------
    crs : str
        Coordinate reference system for the resulting dataset as OGC WKT or
        Proj.4 string, will be passed to Dataset.rio.reproject.
    bounds : (west, south, east, north)
        Extent for the resulting dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.clip_box.
    precipitation : 'chelsa' or 'cw5e5', optional
        Precipitation rate data source, default to same as temperature.
    temperature : 'chelsa' or 'cw5e5', optional
        Near-surface air temperature data source, default to 'chelsa'.
    resolution : float, optional
        Resolution for the output dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.reproject.

    Returns
    -------
    ds : Dataset
        The resulting dataset containing surface variables with the requested
        ``crs``, ``bounds``, and ``resolution``. Use ``ds.to_netcdf()`` to
        export as PISM bootstrapping file.

    Notes
    -----

    The **calendar** is set to 'noleap'. The 365-day year is divided into
    twelve unequal months, including a 28-day February month. This the default
    calendar in PISM. Other calendars could be added in future versions.

    To avoid ambiguity, **time units** are set to 'days'. A Udunits 'year' is
    always 365.242198781 days, not a calendar year. A Udunits 'month' is one
    twelfth of that, not a calendar month. In addition, Python's ``cftime``
    (and thus xarray) does not understand the unit '365 days'.

    CHELSA-2.1 **temperature** and **precipitation rates** are converted to the
    SI **units** 'K' and 'kg m-2 s-1'. According to the CHELSA-2.1
    docs monthly climatologies "represent averages for the calendar month". The
    1981--2010 period contains 6 leap years over 30 years, so the average
    February lasts 28.2 days. Due to the no-leap calendar, February
    precipitations are condensed over a slightly shorter period of 28 days,
    which overestimates daily rates. However, the total amount is unaffected.

    Any **grid_mapping** variable in the source data will be renamed to
    'spatial_ref' to avoid returning a dataset with multiple grid mappings.
    """

    # future parameters:
    # - domain : str, optional
    #     Modelling domain defining geographic projection and bounds.
    # - elevation : 'chelsa', optional
    #     Surface elevation for time-lapse corrections, default to same as
    #     temperature.

    # use temperature source by default
    precipitation = precipitation or temperature

    # open reprojected online data
    temp = _open_climatology(source=temperature, variable='tas')
    temp = _reproject_data_array(temp, crs, bounds, resolution)
    prec = _open_climatology(source=precipitation, variable='pr')
    prec = _reproject_data_array(prec, crs, bounds, resolution)
    elev = _open_elevation(source='chelsa')
    elev = _reproject_data_array(elev, crs, bounds, resolution)

    # combine into dataset
    ds = xr.Dataset({
        'air_temp': temp,
        'precipitation': prec,
        'elevation': elev})

    # assign time coordinate and bounds
    months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    bounds = np.stack([months.cumsum()-months[0], months.cumsum()]).T
    ds = ds.assign_coords(
        time=(('time'), bounds[:, 0]),
        time_bounds=(('time', 'nv'), bounds))
    ds.time.attrs.update(
        bounds='time_bounds', calendar='noleap', units='days since 1-1-1')

    # convert temperature to K
    if temperature == 'chelsa':
        assert 'units' not in ds.air_temp.attrs
        ds['air_temp'] += 273.15
    elif temperature == 'cw5e5':
        assert ds.air_temp.units == 'K'

    # convert precipitation to kg m-2 s-1
    if precipitation == 'chelsa':
        assert 'units' not in ds.precipitation.attrs
        ds['precipitation'] /= (
            3600 * 24 * xr.DataArray(months, coords={'time': ds.time}))
    elif precipitation == 'cw5e5':
        assert ds.precipitation.units == 'kg m-2 s-1'

    # set variable attributes
    ds.air_temp.attrs.update(
        long_name='near-surface air temperature',
        standard_name='air_temperature', units='K')
    ds.precipitation.attrs.update(
        long_name='mean annual precipitation rate',
        standard_name='precipitation_flux', units='kg m-2 s-1')
    ds.elevation.attrs.update(
        long_name='ice surface altitude',
        standard_name='surface_altitude', units='m')

    # clear scaling attributes
    _clear_scaling_attributes(ds)

    # return projected dataset
    return ds


def bootstrap(crs, bounds, bedrock='gebco', resolution=1e3):
    """
    Open bootstrapping data from online datasets for PISM.

    Parameters
    ----------
    crs : str
        Coordinate reference system for the resulting dataset as OGC WKT or
        Proj.4 string, will be passed to Dataset.rio.reproject.
    bounds : (west, south, east, north)
        Extent for the resulting dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.clip_box.
    bedrock : 'chelsa' or 'gebco', optional
        Bedrock altitude data source, default to 'gebco':
        - 'chelsa': global 1-arc-second CHELSA input DEM from GMTED2010.
        - 'gebco': global 15-arc-second elevation data from GEBCO.
    resolution : float, optional
        Resolution for the output dataset in projected coordinates given by
        ``crs``, will be passed to Dataset.rio.reproject.

    Returns
    -------
    ds : Dataset
        The resulting dataset containing surface variables with the requested
        ``crs``, ``bounds``, and ``resolution``. Use ``ds.to_netcdf()`` to
        export as PISM bootstrapping file.

    Notes
    -----

    Any **grid_mapping** variable in the source data will be renamed to
    'spatial_ref' to avoid returning a dataset with multiple grid mappings.
    """

    # future parameters
    # - geoflux : ?, optional
    #     Name of geothermal heat flux dataset, default to none?
    # - thickness : ?, optional
    #     Name of ice thickess dataset, default to none?

    # initialize empty dataset
    ds = xr.Dataset()

    # add reprojected bedrock altitude
    da = _open_elevation(source=bedrock)
    da = _reproject_data_array(da, crs, bounds, resolution)
    da.attrs.update(standard_name='bedrock_altitude')
    ds = ds.assign(bedrock=da)

    # clear scaling attributes
    _clear_scaling_attributes(ds)

    # return projected dataset
    return ds
