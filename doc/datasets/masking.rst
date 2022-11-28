.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Masking and interpolation
=========================

Ice thickness threshold
-----------------------

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
       ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
       for i, value in enumerate([0.1, 1, 500]):
           hyoga.config.glacier_masking_point = value
           ds.hyoga.plot.ice_margin(edgecolor=f'C{i}', linewidths=1)

   # restore the default of 1 m
   hyoga.config.glacier_masking_point = 1


Custom glacier mask
-------------------

For more control, on can set the ``land_ice_area_fraction`` variable using
:meth:`~.Dataset.hyoga.assign_icemask`. Suppose that we define glaciers as grid
cells filled with ice at least a metre thick, and moving at least ten metres
per year:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds = ds.hyoga.assign_icemask(
           (ds.hyoga.getvar('land_ice_thickness') > 1) &
           (ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity') > 10))
       ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
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

Interpolation to another topography
-----------------------------------

For enhanced visuals, hyoga supports interpolating and remasking model output
onto a different (usually higher-resolution) topography. This produces an image
which deviates somewhat from the model results, but with detail potentially
improving readability.

A necessary first step in many cases is to compute the bedrock deformation due
to isostatic adjustment. If the dataset was produced by a model including
bedrock deformation, there will be a systematic offset between the model
bedrock topography and the new topography onto which data are interpolated.

.. warning::
   Assigning isostasy is not strictly necessary for interpolation to succeed,
   but omitting it would produce errors in the new ice mask. Of course, it can
   be safely omitted if the model run does not include isostasy.

In this case, we compute the bedrock deformation by comparing bedrock altitude
in the dataset with bedrock altitude in the initial state:

.. plot::
   :context:
   :nofigs:

   ds = hyoga.open.example('pism.alps.out.2d.nc')
   ds = ds.hyoga.assign_isostasy(hyoga.open.example('pism.alps.in.boot.nc'))

The method :meth:`~.Dataset.hyoga.assign_isostasy` assigns a new variable
(standard name ``bedrock_altitude_change_due_to_isostatic_adjustment``). Next
we run :meth:`~.Dataset.hyoga.interp`
which interpolates all variables, and recalculates an ice mask based on the new
topographies, corrected for bedrock depression in this case. This uses yet
another demo file, which contains high-resolution topographic data over a small
part of the model domain.

.. plot::
   :context:
   :nofigs:

   ds = ds.hyoga.interp(hyoga.open.example('pism.alps.vis.refined.nc'))

The new dataset can be plotted in the same way as any other hyoga dataset, only
with a much higher resolution.

.. plot::
   :context:

   ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
   ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
   ds.hyoga.plot.surface_altitude_contours()
   ds.hyoga.plot.ice_margin(edgecolor='0.25')

.. _xarray: https//xarray.pydata.org
.. _`CF standard names`: http://cfconventions.org/standard-names.html
