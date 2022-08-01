.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Masking and interpolation
=========================

Hyoga already includes a few more tools meant to postprocess data before
plotting. Please refer to the programming interface for their documentation.

.. currentmodule:: xarray

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.assign_isostasy
   Dataset.hyoga.getvar
   Dataset.hyoga.interp
   Dataset.hyoga.where
   Dataset.hyoga.where_thicker

.. _xarray: https//xarray.pydata.org
.. _`CF standard names`: http://cfconventions.org/standard-names.html
