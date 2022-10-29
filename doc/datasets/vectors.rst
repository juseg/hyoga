.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting vector graphics
========================

Hyoga currently supports plotting two types of vector graphics:
`Natural Earth`_ data and Last Glacial Maximum paleoglacier extents.

Natural Earth data
------------------

`Natural Earth`_ is a global, public domain geographic dataset featuring both
vector and raster data. Only vector data are used in hyoga. Natural Earth
vectors are divided in two categories: cultural (countries, populated places,
etc) and physical (rivers, lakes, glaciers, etc), and available at three levels
of detail referred as the scales 1:10m, 1:50m, and 1:110m.

The easiest way to plot Natural Earth as a background for gridded datasets is
through the accessor plot method, :meth:`.Dataset.hyoga.plot.naturalearth`.
Called without arguments it renders a composite map of rivers, lakes, and the
coastline at the highest available scale:

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth()

.. warning::

   To reproject Natural Earth data in the gridded dataset projection, the
   dataset Coordinate Reference System is sought in a ``ds.proj4`` attribute,
   typically a PROJ4 string but possibly any other format understood by
   :meth:`geopandas.GeoDataFrame.to_crs`.

Any other Natural Earth theme from the `Natural Earth downloads`_ page can be
picked, and the usual matplotlib styling keyword arguments are available. For
instance, to plot glaciated areas in blue, use:

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth('glaciated_areas', color='tab:blue')

The method defaults to plotting themes in the ``physical`` category at the
highest scale of ``10m``. Cultural features require a ``category='cultural'``
while lower scales are available through the ``scale`` keyword argument:

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth(
          theme='urban_areas', category='cultural', scale='50m',
          color='tab:orange')

Any number of themes can be plotted in a single method call as long as they
share the same category and scale:

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth(('lakes', 'lakes_europe'))

Hyoga also provides two aliases ``'lakes_all'`` and ``'rivers_all'`` that
respectively plot, well, all lakes and all rivers at ``'10m'`` scale, including
such regional subsets as ``'lakes_europe'``.

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth('rivers_all')

Plotting and reprojection is handled by using :class:`geopandas.GeoDataFrame`
objects in the background, and any additional keywords arguments are passed to
:class:`geopandas.GeoDataFrame.plot`. This examples plots cities colored by
regional significance:

.. plot::

   # plot example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:
      ds.hyoga.plot.bedrock_altitude(center=False)
      ds.hyoga.plot.naturalearth(
          'populated_places', category='cultural',
          column='SCALERANK', cmap='Reds_r')


Opening vector data
-------------------

Sometimes more control is needed, or vectors may be plotted independently of
gridded data. For such cases, hyoga provides functions to open Natural Earth
and paleoglacier vector data for further manipulation.

In the background, accessor plot methods described in previous sections use
:func:`hyoga.open.naturalearth` and :func:`hyoga.open.paleoglaciers` to
download, cache, and open vector data as :class:`geopandas.GeoDataFrame`.
The aforementioned (non-plotting) keyword arguments remain available:

.. plot::

   hyoga.open.naturalearth(theme='urban_areas', category='cultural')
   hyoga.open.paleoglaciers(source='bat19')

Geodataframes inherit :class:`pandas.DataFrame` functionality, and thus provide
a rich interface to subset, manipulate and visualize geographic vector data.
For instance to plot African countries colored by population use:

.. plot::

   gdf = hyoga.open.naturalearth('admin_0_countries', category='cultural')
   gdf[gdf.CONTINENT == 'Africa'].plot('POP_EST', cmap='Greens')

Geodataframes can be re-projected using a variety of coordinate reference
system formats. Plotting Batchelor et al. 2019 paleoglacier extents in arctic
polar stereographic projection (`EPSG 3995`_) is as simple as:

.. plot::

   gdf = hyoga.open.paleoglaciers('bat19')
   gdf.to_crs(3995).plot()

Here is a more advanced example using Natural Earth attribute tables to select
particular features within a theme and plot them with a different colour.

.. plot:: ../examples/cartography/plot_naturalearth_geopandas.py

.. _EPSG 3995: https://epsg.io/3995
.. _Natural Earth: https://www.naturalearthdata.com/
.. _Natural Earth downloads: https://www.naturalearthdata.com/downloads/
