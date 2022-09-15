.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Programming interface
=====================

.. note::

   All functions and methods documented here are considered **public** API.
   They are divided into three modules ``calc``, ``open``, and ``plot``. The
   submodule level (e.g. ``plot.naturalearth``) as well as the ``util`` module,
   are considered **private** implementation detail and may change at anytime.

Configuration
-------------

.. currentmodule:: hyoga

.. autosummary::
   :toctree: generated/

   config

Input - ``hyoga.open``
----------------------

.. autosummary::
   :toctree: generated/

   open.dataset
   open.mfdataset
   open.subdataset

.. future:
   hyoga.open.demo
   hyoga.open.visual?

.. future:
   Computation - ``hyoga.calc``
   ----------------------------
   Masking and interpolation
   ~~~~~~~~~~~~~~~~~~~~~~~~~
   Make dataset computation methods available here?

Visualization - ``hyoga.plot``
------------------------------

.. future:
   Plotting datasets
   ~~~~~~~~~~~~~~~~~
   Make dataset plotting methods available here?

Plotting data arrays
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   hyoga.plot.hillshade

Plotting vector data
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   hyoga.plot.feature
   hyoga.plot.cities
   hyoga.plot.countries
   hyoga.plot.country_borders
   hyoga.plot.states
   hyoga.plot.state_borders
   hyoga.plot.ocean
   hyoga.plot.rivers
   hyoga.plot.graticules
   hyoga.plot.shapefile

.. future:
   hyoga.plot.annotate.polar
   hyoga.plot.annotate.scatter
   hyoga.plot.barscale.barscale

Xarray datasets
---------------

These methods are available on :mod:`xarray` Datasets after ``import hyoga``.

Postprocessing
~~~~~~~~~~~~~~

.. currentmodule:: xarray

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.assign
   Dataset.hyoga.assign_icemask
   Dataset.hyoga.assign_isostasy
   Dataset.hyoga.getvar
   Dataset.hyoga.interp
   Dataset.hyoga.where
   Dataset.hyoga.where_icemask
   Dataset.hyoga.where_thicker

.. future:
   hyoga.calc.profile.build_profile_coords
   hyoga.calc.profile.read_shp_coords

Plotting
~~~~~~~~

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.plot.bedrock_altitude
   Dataset.hyoga.plot.bedrock_altitude_contours
   Dataset.hyoga.plot.bedrock_hillshade
   Dataset.hyoga.plot.bedrock_shoreline
   Dataset.hyoga.plot.bedrock_erosion
   Dataset.hyoga.plot.bedrock_isostasy
   Dataset.hyoga.plot.ice_margin
   Dataset.hyoga.plot.surface_altitude_contours
   Dataset.hyoga.plot.surface_hillshade
   Dataset.hyoga.plot.surface_velocity
   Dataset.hyoga.plot.surface_velocity_streamplot
