.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting glacier data
=====================

Hyoga include several plot methods that make visualizing ice-sheet modelling
datasets a tiny bit more straightforward than using xarray_ alone. While not
a strict requirement, these should ideally be used in combination with cartopy_
geolocated axes. This will allow overlaying geographic information in different
coordinate systems, for instance coming from global vector datasets (see
:doc:`/plotting/vectors`). For this reason, we import a couple of modules:

.. plot::
   :context:
   :nofigs:

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import hyoga.open

Next, we create new axes with a Universal Transverse Mercator zone 32
reference system, corresponding to the example data.

.. plot::
   :context:
   :nofigs:

   ax = plt.subplot(projection=ccrs.UTM(32))

Next, it is time to add data. Let's open an example dataset and plot the
bedrock altitude and a simple ice margin contour:

.. plot::
   :context:

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')

Hyoga provides wrappers around xarray_ and
matplotlib_ methods to produce oft-used ice sheet model plots with a more
practical default style.

.. plot::
   :context:

   # initialize subplot with UTM projection
   ax = plt.subplot(projection=ccrs.UTM(32))
   ds.hyoga.plot.bedrock_altitude(ax=ax, center=False)
   ds.hyoga.plot.ice_margin(ax=ax)

Hyoga tries to infer some missing variables from others present in the dataset.
Here, the velocity norm was reconstructed from its horizontal components. These
computations are done on-the-fly and the results are not stored.

Velocity maps are automatically log-scaled, but the limits can be customized:

.. plot::
   :context:

   ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
   ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
   ds.hyoga.plot.ice_margin(edgecolor='0.25')

.. _cartopy: https://scitools.org.uk/cartopy/
.. _matplotlib: https://matplotlib.org
.. _xarray: https//xarray.pydata.org
