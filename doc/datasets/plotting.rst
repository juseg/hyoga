.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting glacier data
=====================

Hyoga include several plot methods that make visualizing ice-sheet modelling
datasets a tiny bit more straightforward than using xarray_ alone.
Let's open an example dataset and plot the
bedrock altitude and a simple ice margin contour:

.. plot::

   import hyoga

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')

Hyoga provides wrappers around xarray_ and
matplotlib_ methods to produce oft-used ice sheet model plots with a more
practical default style.


Hyoga tries to infer some missing variables from others present in the dataset.
Here, the velocity norm was reconstructed from its horizontal components. These
computations are done on-the-fly and the results are not stored.

Velocity maps are automatically log-scaled, but the limits can be customized:

.. plot::

   import hyoga

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
       ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
       ds.hyoga.plot.ice_margin(edgecolor='0.25')

.. _cartopy: https://scitools.org.uk/cartopy/
.. _matplotlib: https://matplotlib.org
.. _xarray: https//xarray.pydata.org
