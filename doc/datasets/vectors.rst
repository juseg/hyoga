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
          edgecolor='tab:red', facecolor='none')
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

.. _Natural Earth: https://www.naturalearthdata.com/
.. _Natural Earth downloads: https://www.naturalearthdata.com/downloads/
