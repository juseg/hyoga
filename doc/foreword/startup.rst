.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Getting started
===============

Installing hyoga
----------------

Assuming xarray_, geopandas_ and cartopy_ are already installed, I recommend
installing hyoga using pip::

   pip install hyoga

.. _cartopy: https://scitools.org.uk/cartopy/
.. _geopandas: https://geopandas.org
.. _xarray: https://xarray.pydata.org/en/stable/

A first plot
------------

Here is a minimal example that demonstrate hyoga's core plotting functionality.
We open example data and plot the bedrock altitude, an ice margin contour, and
hydrologic features to facilitate orientation.

.. plot::
   :context:

   import matplotlib.pyplot as plt
   import hyoga.open

   # plot example data
   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')
       ds.hyoga.plot.naturalearth()

   # set title
   plt.title('A first plot with hyoga')

.. tip::

   Hyoga alters matplotlib_ defaults with its own style choices. However, these
   choices can always be overriden using matplotlib keyword arguments.

.. _matplotlib: https://matplotlib.org

Then what
---------

Hyoga implements several other methods for :doc:`/plotting/datasets` on any
CF_-compliant xarray_ dataset. Assuming you have own results to explore, try
replacing the example line with::

   import xarray as xr
   xr.open_dataset('yourfile.nc')

.. _CF: https://cfconventions.org

.. FIXME: rethink docs structure following move to geopandas?

To make your maps pop, check out pages on :doc:`/datasets/altitude`,
:doc:`/datasets/vectors`, and :doc:`/datasets/masking`. For a visual overview
of the package capabilities, head directly to the :doc:`/examples/index`.
