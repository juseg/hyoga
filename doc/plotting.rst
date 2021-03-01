.. Copyright (c) 2021, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting glacier data
=====================

Plotting with xarray
--------------------

Let us open the demo data again:

.. ipython:: python

   import hyoga.demo
   import hyoga.open

   ds = hyoga.open.dataset(hyoga.demo.pism_gridded())
   ds = ds.sel(age=24)

Plotting is already quite convenient using xarray:

.. ipython:: python

   ds.topg.plot.imshow(add_colorbar=False)
   (ds.topg+ds.thk).plot.contourf()

   @savefig plot_with_xarray.png
   plt.gca().set_aspect('equal')

Plotting with hyoga
-------------------

To make things even easier, hyoga provides wrappers around xarray_ and
matplotlib_ methods to produce oft-used ice sheet model plots with a more
practical default style:

.. ipython:: python

   ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
   ds.hyoga.plot.surface_altitude_contours()
   @savefig plot_surface_altitude.png
   ds.hyoga.plot.ice_margin(facecolor='w')

As may be noticed in the above code, hyoga plot methods also do the job to
look up required variables (by their standard names) and to infer missing
variables when that is possible. For instance in the above example, the
``'surface_altitude'`` was missing from the data and thus computed from
``'bedrock_altitude'`` and ``'land_ice_thickness'``. Such computations are
done on-the-fly though, and the results are not stored:

.. ipython:: python

   for name, var in ds.items():
      print(name, var.attrs.get('standard_name', None))

Velocity maps are automatically log-scaled, but the limits can be customized:

.. ipython:: python

   ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
   ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
   ds.hyoga.plot.ice_margin(edgecolor='0.25')
   @savefig plot_surface_velocity.png
   plt.gca().set_aspect('equal')


Plotting with cartopy
---------------------

For enhanced visuals, hyoga plots can be georeferenced and combined with
`Natural Earth`_ vector data shipped with cartopy_.

.. ipython:: python

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature

   # initialize subplot with UTM projection
   ax = plt.subplot(projection=ccrs.UTM(32))

   # add coastline and rivers
   ax.coastlines(edgecolor='0.25', linewidth=0.5)
   ax.add_feature(
      cfeature.NaturalEarthFeature(
         category='physical', name='rivers_lake_centerlines', scale='10m'),
      edgecolor='0.25', facecolor='none', linewidth=0.5, zorder=0)

   # plot model output
   ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
   ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
   @savefig plot_with_cartopy.png
   ds.hyoga.plot.ice_margin()

More plotting methods are available. Please take a look at the
:doc:`./examples/index` gallery.


.. _cartopy: https://scitools.org.uk/cartopy/
.. _matplotlib: https://matplotlib.org
.. _xarray: https//xarray.pydata.org
.. _`Natural Earth`: https://www.naturalearthdata.com
.. _`CF standard names`: http://cfconventions.org/standard-names.html
