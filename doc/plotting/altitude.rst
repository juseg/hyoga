.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting altitude maps
======================

Hyoga colormaps
---------------

In addition to the vast selection of matplotlib built-in colormaps_, hyoga
add three custom colormaps for altitude maps (``Topographic``, ``Bathymetric``,
and ``Elevational``) and two half-transparent colormaps for relief-shading
(``Glossy``, and ``Matte``). These new colormaps can be used in any matplotlib
method after importing hyoga.

.. _colormaps: https://matplotlib.org/stable/tutorials/colors/colormaps.html

.. plot:: ../examples/cartography/plot_colormap_reference.py
   :include-source: False

In addition, these colormaps trigger special behaviour when used in some of
hyoga's plot methods. Here is an example plotting bedrock altitude contours for
the example data using the ``Topographic`` colormap for altitude and the
``Glossy`` colormap for hillshades.

.. plot::
   :context:

   import hyoga

   # open example data
   with hyoga.open.example('pism.alps.in.boot.nc') as ds:

       # plot model output
       ds.hyoga.plot.bedrock_altitude_contours(cmap='Topographic', vmin=0)
       ds.hyoga.plot.bedrock_hillshade(cmap='Glossy')

Note how the bedrock altitude contour levels are not equidistant, but are
instead densified at lower elevation to highlight lower reliefs and fit the
highly skewed ``Topographic`` colormap.
