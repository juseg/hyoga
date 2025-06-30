.. Copyright (c) 2021-2025, Julien Seguinot (juseg.dev)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

.. currentmodule:: hyoga

.. What's new sections, cheated on xarray
   - Breaking changes
   - Deprecations
   - New features
   - Bug fixes
   - Documentation
   - Internal changes

.. Guidelines for cross-references
   - Use relative paths for accessor members (:meth:`.Dataset.hyoga.assign`)
   - Use relative paths for class members (:meth:`.Job.submit`)
   - Use absolute paths for module members (:func:`hyoga.open.paleoglaciers`)
   - Use absolute paths for external references (:meth:`xarray.Dataset.assign`)
   - Never use ``~``, as hyoga uses explicit subaccessors and submodules.

What's new
==========

.. _v0.3.2:

v0.3.2 (unreleased)
-------------------

New features
~~~~~~~~~~~~

- Add ``temperature`` and ``precipitation`` arguments, and CHELSA-W5E5_
  (aliased ``'cw5e5'``) as a new temperature and precipitation data source in
  :func:`hyoga.open.atmosphere` (:issue:`86`, :pull:`87`), aggregated on 30x30
  degree tiles (:issue:`88`, :pull:`92`), concatenated yearly (:issue:`99`,
  :pull:`100`), and compressed with netCDF-4 (:issue:`101`, :pull:`102`).

.. _CHELSA-W5E5: https://chelsa-climate.org/chelsa-w5e5-v1-0-daily-climate-data-at-1km-resolution/

Breaking changes
~~~~~~~~~~~~~~~~

- Require Matplotlib 3.5 or newer (:issue:`107`, :pull:`108`).

Bug fixes
~~~~~~~~~

- Add newly missing requirement of ``numpy<2`` (:issue:`90`, :pull:`91`).
- Fix CHELSA_-2.1 download urls (:issue:`103`, :pull:`104`).
- Fix Ehlers et al. (2011) download error (:issue:`109`, :pull:`110`).
- Add Sphinx config path in `.readthedocs.yaml` (:issue:`105`, :pull:`106`).
- Fix broken colormap registration in some recent matplotlib versions
  (:issue:`107`, :pull:`108`).

Internal changes
~~~~~~~~~~~~~~~~

- Add aggregators in :mod:`hyoga.open.aggregator` (:issue:`86`, :issue:`88`,
  :issue:`99`, :issue:`101`, :pull:`87`, :pull:`92`, :pull:`100`, :pull:`102`).

.. _v0.3.1:

v0.3.1 (10 Jun. 2024)
---------------------

This small bug-fix release brings hyoga up-to-date with its dependencies
following an unintended lapse in development. Support was added for recent
versions of Python and cf_xarray_, and other minor bugs were fixed, reviving
the foundation for upcoming improvements and new features in future releases.
Code coverage remains at 67 percent.

Breaking changes
~~~~~~~~~~~~~~~~

- Require Python 3.9 or newer (:pull:`78`).

Deprecations
~~~~~~~~~~~~

- Remove :func:`hyoga.demo.pism_gridded`, deprecated in v0.1.1_ (:pull:`85`).
- Remove :func:`hyoga.demo.pism_series`, deprecated in v0.1.1_ (:pull:`85`).

Bug fixes
~~~~~~~~~

- Add missing optional dependency to dask_ (:issue:`74`, :pull:`76`).
- Fix incompatibility with cf_xarray_ 0.8.0 (:issue:`73`, :pull:`78`).
- Fix multiple mappings in reprojected datasets (:issue:`72`, :pull:`81`).

.. _dask: https://www.dask.org

Documentation
~~~~~~~~~~~~~

- Fix build errors and warnings (:issue:`79`, :pull:`80`).
- Update funding credits (:pull:`80`, :pull:`84`).

Internal changes
~~~~~~~~~~~~~~~~

- Test (and support) Python 3.11 and 3.12 (:pull:`77`).
- Upgrade to Python 3.12 on Read the Docs (:pull:`82`).

.. _v0.3.0:

v0.3.0 Cocuy (16 Jan. 2023)
---------------------------

.. plot:: ../examples/whatsnew/plot_v003_cocuy.py
   :include-source: false

This release turns hyoga into more than just a visualization tool. Two
functions were added to :doc:`open </datasets/opening>` online elevation data
(GEBCO_) and monthly climatologies (CHELSA_) in custom projections that can be
used as PISM_ input files for paleoglacier modelling about anywhere on Earth.
Minor bugs were fixed. Code coverage decreased to 67 percent.

.. _PISM: https://pism.io

Breaking changes
~~~~~~~~~~~~~~~~

- Add rioxarray_ as a required dependency (see new features).

.. _rioxarray: https://corteva.github.io/rioxarray

Deprecations
~~~~~~~~~~~~

- Remove :meth:`.Dataset.hyoga.interp` ``threshold``, deprecated in v0.1.2_.

New features
~~~~~~~~~~~~

- Add :func:`hyoga.open.bootstrap` to open global elevation data from either
  GEBCO_ or CHELSA_ as bootstrapping data for PISM (:issue:`1`, :pull:`51`,
  :issue:`54`, :pull:`55`, :issue:`57`, :pull:`60`, :pull:`62`).
- Add :func:`hyoga.open.atmosphere` to open monthly climatologies from CHELSA_
  as atmospheric data for PISM (:issue:`3`, :pull:`56`).

.. _CHELSA: https://chelsa-climate.org
.. _GEBCO: https://www.gebco.net

Bug fixes
~~~~~~~~~

- Add workaround for scipy 0.10.0 bug in profile interpolation with mixed data
  types (https://github.com/scipy/scipy/issues/17718, :issue:`58`, :pull:`59`).
- Vector plot methods are now compatible with rioxarray CRS and CF grid mapping
  (using ``decode_coords='all'``, :issue:`52`, :pull:`61`).

Documentation
~~~~~~~~~~~~~

- Document opening reprojected bootstrapping and atmospheric online data, and
  rework parts of datasets chapter outline (:issue:`53`, :pull:`63`).

.. _v0.2.2:

v0.2.2 (16 Dec. 2022)
---------------------

This release implements profile :doc:`interpolation <datasets/masking>` and
scale bars, both documented in new :doc:`examples<examples/index>`, and fixes a
bug in grid interpolation to axes coordinates. Continuous integration has been
improved with lazy tests for all plot methods, and monitoring of code coverage,
increased from 33 to 73 percent in this release.

New features
~~~~~~~~~~~~

- Add accessor method :meth:`.Dataset.hyoga.profile`, a new example and a
  documentation section for profile interpolation (:issue:`18`, :pull:`46`).
- Add plot method :meth:`.Dataset.hyoga.plot.scale_bar` and a new example for
  automatically sized, anchored scale bars (:issue:`16`, :pull:`44`).

Bug fixes
~~~~~~~~~

- Fix grid interpolation on non-cartopy axes (:issue:`45`).

Internal changes
~~~~~~~~~~~~~~~~

- Add very simple tests for all plot methods (:issue:`37`, :pull:`49`).
- Compute code coverage and upload to codecov.io (:issue:`38`, :pull:`47`).
- Add docs, tests and codecov badges in readme file (:pull:`48`).
- Add automatic delivery on PyPI (:issue:`39`, :pull:`50`).

.. _v0.2.1:

v0.2.1 (1 Dec. 2022)
--------------------

This release removes the required dependency on cartopy_ by implementing own
downloaders for Natural Earth and other (and future) data. All dependencies,
and the docs, can be built with pip. Plot methods set aspect ratio to equal,
and coordinate labels are hidden by default. Development has moved on a
feature-branch squash workflow (as xarray_ and geopandas_).

.. _xarray: https://xarray.dev

Breaking changes
~~~~~~~~~~~~~~~~

- Require Python 3.8 or newer (see
  `xarray#7115 <https://github.com/pydata/xarray/issues/7115>`_,
  `NEP-29 <https://numpy.org/neps/nep-0029-deprecation_policy.html>`_).

Deprecations
~~~~~~~~~~~~

- Remove :func:`hyoga.open.visual`, deprecated in v0.1.0.
- The ``sealevel`` argument in :meth:`.Dataset.hyoga.plot.bedrock_altitude` is
  deprecated and will be removed in v0.4.0. Use ``center=sealevel`` instead
  (:issue:`27`, :pull:`36`).

New features
~~~~~~~~~~~~

- Remove dependency on cartopy_ (:issue:`25`, :pull:`28`).
- Set aspect ratio equal when plotting datasets (:issue:`26`, :pull:`31`).
- Hide map axes and labels when plotting datasets (:issue:`30`, :pull:`34`).

Bug fixes
~~~~~~~~~

- Add missing required dependency on requests_.

.. _requests: https://requests.readthedocs.io

Documentation
~~~~~~~~~~~~~

- List plot method :meth:`.Dataset.hyoga.plot.bedrock_altitude_contours`
  parameters in docstring (:issue:`33`).
- Homogenize and explain the use of ``center=False`` in documentation pages and
  gallery examples (:issue:`27`, :pull:`36`)

Internal changes
~~~~~~~~~~~~~~~~

- Cache data in ``XDG_CACHE_HOME`` if variable if present in environment.
- Add downloaders in :mod:`hyoga.open.downloader` (:issue:`25`, :pull:`28`).
- Check for shapefile ``.dbf``, ``.prj``, ``.shx`` (:issue:`29`, :pull:`35`).
- Add minimal continuous integration, no tests yet (:pull:`32`).

.. _v0.2.0:

v0.2.0 Bale (1 Nov. 2022)
-------------------------

.. plot:: ../examples/whatsnew/plot_v002_bale.py
   :include-source: false

This is a minor release implementing several cartographic features. It adds
custom colormaps and plot methods for :doc:`shaded reliefs</datasets/shading>`,
and an interface to :doc:`open and plot </datasets/vectors>` Natural Earth data
and paleoglacier extents. The documentation uses a new theme. A logo and new
:doc:`examples <examples/index>` were added. The package structure has been
reworked to better serve :doc:`future plans <roadmap>`.

Breaking changes
~~~~~~~~~~~~~~~~

- Add new required dependencies on cartopy_ and geopandas_. Cartopy is only
  used to download `Natural Earth`_ data, and may no longer be required in
  future versions (:issue:`25`).

.. _cartopy: https://scitools.org.uk/cartopy/
.. _geopandas: https://geopandas.org
.. _Natural Earth: https://www.naturalearthdata.com/

Deprecations
~~~~~~~~~~~~

- Function :func:`hyoga.demo.get` (returning an url) is deprecated, use
  :func:`hyoga.open.example` (returning a dataset) instead.

New features
~~~~~~~~~~~~

- Add three altitude (``Topographic``, ``Bathymetric``, ``Elevational``) and
  two relief-shading (``Glossy``, ``Matte``) colormaps, and correponding color
  lists, accessible through the matplotlib colormap register (:issue:`15`).
- Add plot methods :meth:`.Dataset.hyoga.plot.bedrock_hillshade` and
  :meth:`.Dataset.hyoga.plot.surface_hillshade` for relief shading
  (:issue:`19`).
- Add plot method :meth:`.Dataset.hyoga.plot.bedrock_altitude_contours`
  for bedrock altitude filled contours, best used in combination with new
  altitude colormaps.
- Add plot method :meth:`.Dataset.hyoga.plot.natural_earth` to add global
  `Natural Earth`_ data through geopandas_ (:issue:`17`).
- Add plot method :meth:`.Dataset.hyoga.plot.paleoglaciers` to add Last
  Glacial Maximum paleoglacier extents through geopandas_ (:issue:`21`).
- Add functions :func:`hyoga.open.natural_earth` and
  :func:`hyoga.open.paleoglaciers` to open global `Natural Earth`_ data and
  Last Glacial Maximum paleoglacier extents as :class:`geopandas.GeoDataFrame`
  (:issue:`24`).

Documentation
~~~~~~~~~~~~~

- Add self-plotted logo, see :doc:`examples/logos/index` (:issue:`20`).
- Add a documentation page for :doc:`foreword/startup`.
- Add a documentation page on :doc:`datasets/shading`, including colormaps
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

.. _v0.1.2:

v0.1.2 (1 Aug 2022)
-------------------

This release includes better masks and a dependency on cf_xarray_.
Plot methods now search for standard variable `land_ice_area_fraction` for
masking and default to using a configurable ice thickness masking point.
Masking with `where` remains available and a new documentation page explains
:doc:`datasets/masking` features.

Breaking changes
~~~~~~~~~~~~~~~~

- Method :meth:`.Dataset.hyoga.assign_isostasy` now returns a copy
  without affecting the original data. This behaviour is consistent with
  :meth:`xarray.Dataset.assign`.
- Method :meth:`.Dataset.hyoga.assign_isostasy` overrides any variable
  with standard name "bedrock_altitude_change_due_to_isostatic_adjustment"
  instead of creating a new variable with the same standard name. This is
  again consistent with :meth:`xarray.Dataset.assign`.

Deprecations
~~~~~~~~~~~~

- The ``threshold`` argument in :meth:`.Dataset.hyoga.interp` is deprecated
  and will be removed in v0.3. Use the ``glacier_masking_point`` parameter in
  :obj:`hyoga.config` or an ice mask instead (see new features).

New features
~~~~~~~~~~~~

- Plot methods now look for ``land_ice_area_fraction`` (instead of
  ``land_ice_thickness``) to determine which grid cells are glacierized.
- Add accessor method :meth:`.Dataset.hyoga.assign` to assign new
  variables by CF-compliant standard names.
- Add accessor method :meth:`.Dataset.hyoga.assign_icemask` to assign an
  ice mask variable with standard name ``land_ice_area_fraction``.
- Add accessor method :meth:`.Dataset.hyoga.where_icemask` to filter
  glacier variable according to ``land_ice_area_fraction``.
- Add :obj:`hyoga.config` with a ``glacier_masking_point`` config parameter, an
  ice thickness threshold used as a fallback if ``land_ice_area_fraction`` is
  missing in the dataset.

Internal changes
~~~~~~~~~~~~~~~~

- Method :meth:`.Dataset.hyoga.getvar` now uses cf_xarray_ to retrieve
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

.. _v0.1.1:

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
  deprecated. Use ``demo.get('pism.alps.out.2d')`` and
  ``demo.get('pism.alps.out.1d')`` instead.

Bug fixes
~~~~~~~~~

- Assign surface altitude during :meth:`.Dataset.hyoga.interp` if it is
  missing, as it is needed to compute the interpolated ice mask.
- Fix :meth:`.Dataset.hyoga.assign_isostasy` and :meth:`.Dataset.hyoga.interp`
  in the case when a dataset (or a data array) is used instead of a file.
- Ensure that :meth:`.Dataset.hyoga.where` and
  :meth:`.Dataset.hyoga.where_thicker` return a copy without affecting the
  original dataset (as :meth:`xarray.Dataset.where`).


Documentation
~~~~~~~~~~~~~

- Examples in the documentation use smaller files currently hosted in a
  separate Github repository `hyoga-data <https://github/juseg/hyoga-data>`_
  (:issue:`11`). You may want to delete the previous, 400 MB file in
  ``~/.cache/hyoga``.
- New examples have been added to demonstrate plotting bedrock isostasy and
  interpolated model output (:doc:`examples/index`, :issue:`11`).

.. _v0.1.0:

v0.1.0 Akaishi (1 Mar 2021)
---------------------------

.. plot:: ../examples/whatsnew/plot_v001_akaishi.py
   :include-source: false

Nothing is old, everything is new. This is the first version!
