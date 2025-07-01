.. Copyright (c) 2021-2025, Julien Seguinot (juseg.dev)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Opening datasets
================

Reading local files
-------------------

Hyoga acts as a thin wrapper around a much more powerful Python library called
xarray_. Xarray is used to open a dataset that can be processed by hyoga.
Typically this will be a local netCDF file as in the example below, but it
could also be a raster file, an online store or a huge dataset spread across
hundreds of files. Whatever the source, xarray does the hard work and provides
us with a :class:`xarray.Dataset` object ready to use with hyoga::

   import xarray as xr
   ds = xr.open_dataset('yourfile.nc')

.. note::

   Hyoga also provides functions to open datasets with an age coordinate in ka
   (see :ref:`api`). However, if possible I recommend to stick with xarray
   functions for the time being.

Opening online data
-------------------

A central functionality for hyoga consists in opening web-available data in
custom projections for numerical ice-sheet modelling. Internally, hyoga will
download the original data, typically global, store a copy in the cache
directory (``~/.cache/hyoga/``), reproject to the desired modelling domain, and
return an :class:`xarray.Dataset`.

Currently two types of input datasets are supported: bootstrapping and
atmospheric, respectively returned by :func:`hyoga.open.bootstrap` and
:func:`hyoga.open.atmosphere`. The bootstrapping data contains bedrock and/or
surface topography. The atmosphere data contains a monthly climatology of air
temperature and precipitation needed to force a positive degree-day model.
This nomenclature follows that introduced by PISM, and the resulting datasets
are ready to export as PISM input files using :meth:`.Dataset.to_netcdf`.

.. warning::

   Running these for the first time will download and deflate ca. 12 GB global
   data in the default case, and ca. 1.2 TB in the case of `cw5e5` atmosphere
   source. Broken or partially downloaded files are not handled and instead
   need to be manually deleted from the cache directory (``~/.cache/hyoga``) in
   case of interrupted downloads.

PISM example run
----------------

The following EPSG code and coordinate bounds describe a Universal Transverse
Mercator (UTM) zone 32 projection covering the European Alps. This is the
format for the data used in the :doc:`/examples/index`. ::

   import hyoga

   # UTM-32 projection, WGS 84 datum
   crs = 'epsg:32632'

   # west, south, east, north bounds
   bounds = [150e3, 4820e3, 1050e3, 5420e3]

The following will prepare a simple bootstrapping dataset containing bedrock
topography from GEBCO_ with a horizontal resolution of a 1 km, and save it to
a PISM-readable NetCDF file::

   ds = hyoga.open.bootstrap(crs=crs, bounds=bounds, resolution=1000)
   ds.to_netcdf('boot.nc')

For the atmospheric forcing, we reduce the input air temperature by six degrees
to simulate glacial conditions. The resulting file contains 24 high-resolution,
monthly temperature and precipitation grid from CHELSA_, hence reprojecting the
data can take several minutes. ::

   ds = hyoga.open.atmosphere(crs=crs, bounds=bounds, resolution=1000)
   ds['air_temp'] -= 6
   ds.to_netcdf('atm.nc')

Both input files are now ready to be used in a simple paleo-glacier modelling
run on the alps::

   mpiexec -n 4 pism \
       -i boot.nc -bootstrap -o run.nc -ys 0 -ye 100 \
       -atmosphere given,elevation_change \
           -atmosphere.given.periodic \
           -atmosphere_given_file atm.nc \
           -atmosphere_lapse_rate_file atm.nc \
       -surface pdd

Since the input data are global, the ``crs`` and ``bounds`` can be modified to
run this setup anywhere on Earth. The results can be viewed in e.g. ``ncview``,
or plotted in hyoga using functionality described in the following pages.

.. _xarray: https//xarray.pydata.org
.. _CHELSA: https://chelsa-climate.org
.. _GEBCO: https://www.gebco.net
