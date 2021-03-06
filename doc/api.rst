.. Copyright (c) 2021, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Programming interface
=====================

Input functions
---------------

.. currentmodule:: hyoga

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

.. NOTE: some method names are too long for the left column but they will look
.. better after including subsections (or importing them at the top level).

.. currentmodule:: xarray

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.assign_isostasy
   Dataset.hyoga.getvar
   Dataset.hyoga.interp
   Dataset.hyoga.where
   Dataset.hyoga.where_thicker

Plotting
~~~~~~~~

.. NOTE: this will work in next versions of sphinx_autosummary_accessors.
   currentmodule:: xarray
   autosummary::
   :toctree: generated/
   :template: subaccessor_method.rst

   Dataset.hyoga.plot.bedrock_altitude

These methods can be accessed under the ``.hyoga.plot`` attribute of xarray
datasets after importing hyoga:

.. currentmodule:: hyoga.plot

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   HyogaPlotMethods.bedrock_altitude
   HyogaPlotMethods.bedrock_shoreline
   HyogaPlotMethods.bedrock_erosion
   HyogaPlotMethods.bedrock_isostasy
   HyogaPlotMethods.ice_margin
   HyogaPlotMethods.surface_altitude_contours
   HyogaPlotMethods.surface_velocity
   HyogaPlotMethods.surface_velocity_streamplot
