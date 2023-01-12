.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Opening datasets
================

Reading output files
--------------------

Hyoga acts as a thin wrapper around a much more powerful Python library called
xarray_. Xarray is used to open a dataset that can be processed by hyoga.
Typically this will be a local netCDF file as in the example below, but it
could also be a raster file, an online store or a huge dataset spread across
hundreds of files. Whatever the source, xarray does the hard work and provides
us with a :class:`xarray.Dataset` object ready to use with hyoga::

   import xarray as xr
   ds = xr.open_dataset('yourfile.nc')

However, for the sake of this documentation, we use an example dataset. This
will download a PISM output file from an online repository, and store it into a
``~/.cache/hyoga`` directory so that it can be reused the next time.

.. plot::
   :context:
   :nofigs:

   import hyoga
   ds = hyoga.open.example('pism.alps.out.2d.nc')

.. note::

   Hyoga also provides functions to open datasets with an age coordinate in ka
   (see :ref:`api`). However, if possible I recommend to stick with xarray
   functions for the time being.
