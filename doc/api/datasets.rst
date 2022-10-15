.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Datasets - ``ds.hyoga``
=======================

Hyoga adds functionality to manipulate and visualize :class:`xarray.Dataset`
objects using a special ``.hyoga`` attribute called dataset accessor. These
methods are available on any xarray dataset after running ``import hyoga``.

Postprocessing
--------------

.. currentmodule:: xarray.Dataset.hyoga
.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   assign
   assign_icemask
   assign_isostasy
   getvar
   interp
   where
   where_icemask
   where_thicker

.. future:
   calc.profile.build_profile_coords
   calc.profile.read_shp_coords

Plotting datasets
-----------------

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   plot.bedrock_altitude
   plot.bedrock_altitude_contours
   plot.bedrock_hillshade
   plot.bedrock_shoreline
   plot.bedrock_erosion
   plot.bedrock_isostasy
   plot.ice_margin
   plot.surface_altitude_contours
   plot.surface_hillshade
   plot.surface_velocity
   plot.surface_velocity_streamplot


Plotting vectors
----------------

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   plot.naturalearth
