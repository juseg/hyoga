.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Getting started
===============

Installing hyoga
----------------

Assuming xarray_ and cartopy_ are already installed, I recommend installing
hyoga using pip::

   pip install hyoga

.. _cartopy: https://scitools.org.uk/cartopy/
.. _xarray: https://xarray.pydata.org/en/stable/

Plotting datasets
-----------------

To make a first plot, let's import some modules:

.. plot::
   :context:
   :nofigs:

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import hyoga.open


Hyoga plots work best in combination with cartopy_ geo-located axes. Here, we
create new axes with a Universal Transverse Mercator zone 32 projection:

.. plot::
   :context:
   :nofigs:

   ax = plt.subplot(projection=ccrs.UTM(32))

It is time to add data. Let's open an example dataset and plot the bedrock
altitude and a simple ice margin contour:

.. plot::
   :context:

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')

Hyoga implements several other methods for :doc:`/plotting/datasets` on any
CF_-compliant xarray_ dataset. Assuming you have own results to explore, try
replacing the example line with::

   import xarray as xr
   xr.open_dataset('yourfile.nc')

.. _CF: https://cfconventions.org

.. _matplotlib: https://matplotlib.org

.. tip::

   Hyoga alters matplotlib default with its own style choices. However, these
   choices can always be overriden using matplotlib keyword arguments.

Adding map elements
-------------------

The map background looks a bit plain. Let us add a few geographic elements to
facilitate orientation, and a better title:

.. plot::
   :context:

   # add coastlines and rivers
   hyoga.plot.coastline(ax=ax)
   hyoga.plot.rivers(ax=ax)
   hyoga.plot.lakes(ax=ax)

   # set title
   ax.set_title('A first plot with hyoga')

Hyoga has several other functions for :doc:`/plotting/altitude`, such as country
borders and paleoglacier extents from global datasets.
