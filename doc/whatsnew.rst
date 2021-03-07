.. Copyright (c) 2021, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

.. currentmodule:: hyoga

.. What's new sections, cheated on xarray
   - Breaking changes
   - Deprecations
   - New Features
   - Bug fixes
   - Documentation
   - Internal Changes


What's new
==========

v0.1.1
------

This release includes a minor bug fix and several documentation improvements.


Deprecations
~~~~~~~~~~~~

- Functions :func:`demo.pism_gridded` and :func:`demo.pism_series` are
  deprecated. Use ``demo.get('pism.alps.out.2d')`` and
  ``demo.get('pism.alps.out.1d')`` instead.


Bug fixes
~~~~~~~~~

- Assign surface altitude during :meth:`HyogaDataset.interp` if it is missing,
  as it is needed to compute the interpolated ice mask.
- Fix :meth:`HyogaDataset.assign_isostasy` and :meth:`HyogaDataset.interp` for
  when a dataset (or data array) is used instead of a file.
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


v0.1.0 "Akaishi"
----------------

Nothing is old, everything is new. This is the first version!
