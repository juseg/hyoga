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

v0.2 (unreleased)
-----------------

New features
~~~~~~~~~~~~

- Add three altitude (``Topographic``, ``Bathymetric``, ``Elevational``) and
  two relief-shading (``Glossy``, ``Matte``) colormaps, and correponding color
  lists, accessible through the matplotlib colormap register, and listed in
  :data:`hyoga.plot.COLORMAPS` and :data:`hyoga.plot.SEQUENCES` (:issue:`15`).
- Add plot function :func:`hyoga.plot.hillshade`, and dataset plot methods
  :meth:`xarray.Dataset.hyoga.plot.bedrock_hillshade` and
  :meth:`xarray.Dataset.hyoga.plot.surface_hillshade` for relief shading
  (:issue:`19`).
- Add plot method :meth:`xarray.Dataset.hyoga.plot.bedrock_altitude_contours`
  for bedrock altitude filled contours, best used in combination with new
  altitude colormaps.
- Add plot function :func:`hyoga.plot.shapefile` allowing speed improvements
  over cartopy_, and highlighting a particular subject (:issue:`17`).

.. FIXME and ignoring duplicates

- Add plot functions :func:`hyoga.plot.feature`, :func:`hyoga.plot.cities`,
  :func:`hyoga.plot.countries`, :func:`hyoga.plot.country_borders`,
  :func:`hyoga.plot.states`, :func:`hyoga.plot.state_borders`,
  :func:`hyoga.plot.coastline`, :func:`hyoga.plot.glaciers`,
  :func:`hyoga.plot.graticules`, :func:`hyoga.plot.lakes`,
  :func:`hyoga.plot.ocean`, and :func:`hyoga.plot.rivers` for `Natural Earth`_
  data through cartopy_.


.. _cartopy: https://scitools.org.uk/cartopy/
.. _Natural Earth: https://www.naturalearthdata.com/

Documentation
~~~~~~~~~~~~~

- Add a documentation page for :doc:`foreword/startup`.
- Add a documentation page on :doc:`plotting/altitude`, including colormaps
  (:issue:`15`).
- Change to Sphinx book_ theme, rework :ref:`api`.

.. _book: https://sphinx-book-theme.readthedocs.io

Internal changes
~~~~~~~~~~~~~~~~

- Move dataset accessor to :mod:`hyoga.core.accessor`.
- Move hyoga configuration to :mod:`hyoga.core.config`.
- Move function to open example data to :mod:`hyoga.open.example`.
- Move functions to open local files to :mod:`hyoga.open.local`.
- Move dataset plot methods to :mod:`hyoga.plot.datasets`.


v0.1.2 (1 Aug 2022)
-------------------

This release includes better masks and a dependency on cf_xarray_.
Plot methods now search for standard variable `land_ice_area_fraction` for
masking and default to using a configurable ice thickness masking point.
Masking with `where` remains available and a new documentation page explains
:doc:`datasets/masking` features.

Breaking changes
~~~~~~~~~~~~~~~~

- Method :meth:`xarray.Dataset.hyoga.assign_isostasy` now returns a copy
  without affecting the original data. This behaviour is consistent with
  :meth:`xarray.Dataset.assign`.
- Method :meth:`xarray.Dataset.hyoga.assign_isostasy` overrides any variable
  with standard name "bedrock_altitude_change_due_to_isostatic_adjustment"
  instead of creating a new variable with the same standard name. This is
  again consistent with :meth:`xarray.Dataset.assign`.

Deprecations
~~~~~~~~~~~~

- The ``threshold`` argument in :meth:`xarray.Dataset.hyoga.interp` is deprecated
  and will be removed in v0.3. Use the ``glacier_masking_point`` parameter in
  :obj:`hyoga.config` or an ice mask instead (see new features).

New features
~~~~~~~~~~~~

- Plot methods now look for ``land_ice_area_fraction`` (instead of
  ``land_ice_thickness``) to determine which grid cells are glacierized.
- Add accessor method :meth:`xarray.Dataset.hyoga.assign` to assign new
  variables by CF-compliant standard names.
- Add accessor method :meth:`xarray.Dataset.hyoga.assign_icemask` to assign an
  ice mask variable with standard name ``land_ice_area_fraction``.
- Add accessor method :meth:`xarray.Dataset.hyoga.where_icemask` to filter
  glacier variable according to ``land_ice_area_fraction``.
- Add :obj:`hyoga.config` with a ``glacier_masking_point`` config parameter, an
  ice thickness threshold used as a fallback if ``land_ice_area_fraction`` is
  missing in the dataset.

Internal changes
~~~~~~~~~~~~~~~~

- Method :meth:`xarray.Dataset.hyoga.getvar` now uses cf_xarray_ to retrieve
  data variables by their standard name. Thus cf_xarray_ is now a required
  dependency (:issue:`12`).
- Add module :mod:`hyoga.conf` implementing a ``config`` object to store
  additional parameters in the future.

.. _cf_xarray: https://cf-xarray.readthedocs.io

Documentation
~~~~~~~~~~~~~

- A new documentation page shortly explains :doc:`datasets/masking` features.
- A new example has been added to show that interpolation also works when
  surface topography is provided instead of bedrock topography.

v0.1.1 (8 Mar 2021)
-------------------

This release includes bug fixes and documentation improvements, including more
lightweight demo data. There are new examples in the gallery demonstrating the
computation of bedrock isostatic adjustment from a reference topography, and
interpolating model results on higher-resolution topography for enhanced
visualization.

Deprecations
~~~~~~~~~~~~

- Functions :func:`demo.pism_gridded` and :func:`demo.pism_series` are
  deprecated. Use ``open.example('pism.alps.out.2d')`` and
  ``open.example('pism.alps.out.1d')`` instead.


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
