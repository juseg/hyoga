.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Masking and selection
=====================

Selecting variables
-------------------

Xarray itself provides powerful ways to explore, index, subset and aggregate
datasets. Here again hyoga is only adding a thin layer of functionality. As
soon as hyoga (or any submodule) has been imported, this new functionality will
be available in a special ``.hyoga`` attribute called "dataset accessor":

.. plot::
   :context:
   :nofigs:

   import hyoga
   ds = hyoga.open.example('pism.alps.out.2d.nc')
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

Masking variables
-----------------

Hyoga's plot methods use an ice mask to determine which grid cells are
glacierized and which are not. According to CF conventions, this is defined by
the standard variable ``land_ice_area_fraction``. There are several ways to
affect the ice mask. The easiest way is to use the (currently single) parametre
in :obj:`hyoga.config`::

   hyoga.config.glacier_masking_point

If the ``land_ice_area_fraction`` variable is missing from the dataset, hyoga
falls back to compute and ice mask from ``land_ice_thickness``, using this
parametre as an ice thickness threshold. The default value is 1 (metre). For
PISM output files, a non-zero threshold may be advisable in case winter output
files contain a thin cover of "seasonal ice" outside the glacier margin, as is
the case in the demo files.

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       for i, value in enumerate([0.1, 1, 500]):
           hyoga.config.glacier_masking_point = value
           ds.hyoga.plot.ice_margin(edgecolor=f'C{i}', linewidths=1)

   # restore the default of 1 m
   hyoga.config.glacier_masking_point = 1

For more control, on can set the ``land_ice_area_fraction`` variable using
:meth:`~.Dataset.hyoga.assign_icemask`. Suppose that we define glaciers as grid
cells filled with ice at least a metre thick, and moving at least ten metres
per year:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds = ds.hyoga.assign_icemask(
           (ds.hyoga.getvar('land_ice_thickness') > 1) &
           (ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity') > 10))
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')

Note that the :meth:`~.Dataset.hyoga.assign_icemask` method edits (or add) a
``land_ice_area_fraction`` variable without affecting the rest of the dataset.
Such lossless masking is should be enough for internal use within Hyoga.
However in some situations, a lossy (destructive) ice mask may be more useful.
This includes exporting data to a compressed netCDF file for the web, where
having homogeneous values outside the glacier mask can greatly reduce file
size. This can be achieved with :meth:`.Dataset.hyoga.where`,
:meth:`~.Dataset.hyoga.where_icemask`, and
:meth:`~.Dataset.hyoga.where_thicker`.
These methods behave like :meth:`xarray.Dataset.where`: they replace data
values with `np.nan` outside the where condition. However, they are meant to
only affect "glacier variables" (currently any variable whose standard name
does not start with ``bedrock_altitude``).
