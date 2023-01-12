.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
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

Currently two types of input datasets are supported: "bootstrapping" and
"atmospheric". The bootstrapping file contains bedrock and/or surface
topography. The atmosphere file contains a monthly climatology of air
temperature and precipitation needed to force a positive degree-day model.
This nomenclature follows that introduced by PISM, and the resulting datasets
are ready to export as PISM input files using :meth:`.Dataset.to_netcdf`.

.. currentmodule:: hyoga.open

.. autosummary::
   :toctree: generated/

   atmosphere
   bootstrap

.. warning::

   Running these for the first time will download and deflate ca. 12 GB data
   from the web. Broken or partially downloaded files are not handled and will
   need to be manually deleted from the cache directory (``~/.cache/hyoga``) in
   case of interrupted downloads.

.. _xarray: https//xarray.pydata.org
