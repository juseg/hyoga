.. Copyright (c) 2021, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Programming interface
=====================

Dataset accessor
----------------

.. NOTE: some method names are too long for the left column but they will look
.. better after including subsections (or importing them at the top level).

.. currentmodule:: hyoga.hyoga

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   HyogaDataset
   HyogaDataset.assign_isostasy
   HyogaDataset.getvar
   HyogaDataset.interp
   HyogaDataset.where
   HyogaDataset.where_thicker

Input functions
---------------

.. currentmodule:: hyoga.open

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   dataset
   mfdataset
   subdataset
   visual

Plot methods
------------

.. currentmodule:: hyoga.plot

.. autosummary::
   :toctree: generated/
   :nosignatures:
   :recursive:

   HyogaPlotMethods
   HyogaPlotMethods.bedrock_altitude
   HyogaPlotMethods.bedrock_shoreline
   HyogaPlotMethods.bedrock_erosion
   HyogaPlotMethods.bedrock_isostasy
   HyogaPlotMethods.ice_margin
   HyogaPlotMethods.surface_altitude_contours
   HyogaPlotMethods.surface_velocity
   HyogaPlotMethods.surface_velocity_streamplot
