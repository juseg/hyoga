.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Programming interface
=====================

Configuration
-------------

.. currentmodule:: hyoga

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   config

Input functions
---------------

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   open.dataset
   open.mfdataset
   open.subdataset

Datasets
--------

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

Plotting
~~~~~~~~

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.plot.bedrock_altitude
   Dataset.hyoga.plot.bedrock_shoreline
   Dataset.hyoga.plot.bedrock_erosion
   Dataset.hyoga.plot.bedrock_isostasy
   Dataset.hyoga.plot.ice_margin
   Dataset.hyoga.plot.surface_altitude_contours
   Dataset.hyoga.plot.surface_velocity
   Dataset.hyoga.plot.surface_velocity_streamplot
