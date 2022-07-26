.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

.. currentmodule:: hyoga

.. What's new sections, cheated on xarray
   - Breaking changes
   - Deprecations
   - New features
   - Bug fixes
   - Documentation
   - Internal changes


What's new
==========

v0.1.2 (unreleased)
-------------------

Breaking changes
~~~~~~~~~~~~~~~~

- Method :meth:`xarray.Dataset.hyoga.assign_isostasy` now returns a copy
  without affecting the original data. This behaviour is consistent with
  :meth:`xarray.Dataset.assign`.

New features
~~~~~~~~~~~~

- Add :meth:`xarray.Dataset.hyoga.assign_icemask`.
- Add :meth:`xarray.Dataset.hyoga.where_icemask`.
- Plot methods look for variable `land_ice_area_fraction`.

Internal changes
~~~~~~~~~~~~~~~~

- Method :meth:`xarray.Dataset.hyoga.getvar` now uses cf_xarray_ to retrieve
  data variables by their standard name. Thus cf_xarray_ is now a required
  dependency (:issue:`12`).

.. _cf_xarray: https://cf-xarray.readthedocs.io

Documentation
~~~~~~~~~~~~~

- A new example has been added to show that interpolation also works when
  surface topography is provided instead of bedrock topography.

v0.1.1 (8 Mar 2021)
-------------------

This release includes bug fixes and several documentation improvements.


Deprecations
~~~~~~~~~~~~

- Functions :func:`demo.pism_gridded` and :func:`demo.pism_series` are
  deprecated. Use ``demo.get('pism.alps.out.2d')`` and
  ``demo.get('pism.alps.out.1d')`` instead.


Bug fixes
~~~~~~~~~

- Assign surface altitude during :meth:`xarray.Dataset.hyoga.interp` if it is missing,
  as it is needed to compute the interpolated ice mask.
- Fix :meth:`xarray.Dataset.hyoga.assign_isostasy` and
  :meth:`xarray.Dataset.hyoga.interp` in the case when a dataset (or a data
  array) is used instead of a file.
- Ensure that :meth:`xarray.Dataset.hyoga.where` and
  :meth:`xarray.Dataset.hyoga.where_thicker` return a copy without affecting
  the original dataset (as :meth:`xarray.Dataset.where`).


Documentation
~~~~~~~~~~~~~

- Examples in the documentation use smaller files currently hosted in a
  separate Github repository `hyoga-data <https://github/juseg/hyoga-data>`_
  (:issue:`11`). You may want to delete the previous, 400 MB file in
  ``~/.cache/hyoga``.
- New examples have been added to demonstrate plotting bedrock isostasy and
  interpolated model output (:doc:`examples/index`, :issue:`11`).


v0.1.0 Akaishi (1 Mar 2021)
---------------------------

Nothing is old, everything is new. This is the first version!
