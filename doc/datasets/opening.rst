.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Reading model output
====================

Opening output files
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

   import hyoga.open
   ds = hyoga.open.example('pism.alps.out.2d.nc')

.. note::

   Hyoga also provides functions to open datasets with an age coordinate in ka
   (see :ref:`api`). However, if possible I recommend to stick with xarray
   functions for the time being.

Selecting variables
-------------------

Xarray itself provides powerful ways to explore, index, subset and aggregate
datasets. Here again hyoga is only adding a thin layer of functionality. As
soon as hyoga (or any submodule) has been imported, this new functionality will
be available in a special ``.hyoga`` attribute called "dataset accessor":

.. plot::
   :context:
   :nofigs:

   ds.hyoga

One thing to note in particular, is that hyoga never accesses model variables
by their "short names". For instance, while ``thk``, refers to the ice
thickness in PISM, it may refer to a different quantity, or to nothing at all,
in another ice-sheet model. This is where `CF standard names`_ come into play.
To access ice thickness by its standard name you may use:

.. plot::
   :context:
   :nofigs:

   var = ds.hyoga.getvar('land_ice_thickness')

If a particular variable is missing, hyoga will additionally try to reconstruct
it from others, such as the sum of bedrock altitude and ice thickness for
surface altitude, or the norm of velocity components for its magnitude.

.. plot::
   :context:
   :nofigs:

   ds.hyoga.getvar('surface_altitude')
   ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity')

This mechanism can be disabled using ``infer=False``. Because surface altitude
is not actually present in the example dataset, the following would raise an
exception::

   ds.hyoga.getvar('surface_altitude', infer=False)

Because `CF standard names`_ for land ice variables are relatively recent,
older ice sheet models may not include them in output metadata. For PISM, a
mechanism has been implemented to fill (some of) these missing standard names
during initialization.

.. note::

   While hyoga has only been tested with PISM so far, I hope it
   will become compatible with some other glacier and ice sheet models in the
   future. If you want to make your glacier model compatible with hyoga, please
   consider implementing `CF standard names`_.

Adding new variables
--------------------

New variables can be added using using xarray_'s dictionary interface or
methods such as :meth:`xarray.Dataset.assign`. Besides, hyoga provides a
dataset method to assign new variables by their standard name.

.. plot::
   :context:
   :nofigs:

   bedrock = ds.hyoga.getvar('bedrock_altitude')
   thickness = ds.hyoga.getvar('land_ice_thickness')
   surface = bedrock + thickness
   new = ds.hyoga.assign(surface_altitude=surface)

This returns a new dataset including the surface altitude variable. Some
control on the variable (short) name can be achieved by preceding the
``assign`` call with :meth:`xarray.DataArray.rename`.

.. plot::
   :context:
   :nofigs:

   surface = surface.rename('surface')
   ds = ds.hyoga.assign(surface_altitude=surface)
   assert 'surface' in ds

However, this only works if the data does not already contain a variable with
the standard name ``surface_altitude``. In that case, that variable's data is
quietly replaced, and the variable is not renamed.

.. plot::
   :context:
   :nofigs:

   surface = surface.rename('name_to_ignore')
   ds = ds.hyoga.assign(surface_altitude=surface)
   assert 'name_to_ignore' not in ds

.. _xarray: https//xarray.pydata.org
.. _`CF standard names`: http://cfconventions.org/standard-names.html
