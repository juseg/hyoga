.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Plotting glacier data
=====================

Plot methods
------------

Hyoga include several plot methods that make visualizing ice-sheet modelling
datasets a tiny bit more straightforward than using xarray_ alone.
Let's open an example dataset and plot the
bedrock altitude and a simple ice margin contour:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='tab:blue')

   # needed to avoid distortion
   plt.gca().set_aspect('equal')

Hyoga alters matplotlib_ defaults with its own style choices. However, these
choices can always be overridden using matplotlib keyword arguments.
Accessor plot methods such as :meth:`~.Dataset.hyoga.plot.bedrock_altitude` and
:meth:`~.Dataset.hyoga.plot.ice_margin` make internal use of
:meth:`.Dataset.hyoga.getvar` to access relevant variables by their
``'standard_name'`` attribute. Here is an example showing variables could
literally be called anything or whatever and still plot:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds = ds.rename(topg='anything', thk='whatever')
       ds.hyoga.plot.bedrock_altitude(cmap='Topographic', center=False)
       ds.hyoga.plot.ice_margin(facecolor='white')

   # needed to avoid distortion
   plt.gca().set_aspect('equal')

Inferring variables
-------------------

Some missing variables can be reconstructed from others present in the dataset
(see :doc:`/datasets/opening`). For instance velocity norms are reconstructed
from their horizontal components. They plot on a logarithmic scale by default,
but the limits can be customized:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(vmin=0, vmax=4500)
       ds.hyoga.plot.surface_velocity(vmin=1e1, vmax=1e3)
       ds.hyoga.plot.ice_margin(edgecolor='0.25')

   # needed to avoid distortion
   plt.gca().set_aspect('equal')

Similarly, :meth:`.Dataset.hyoga.plot.surface_velocity_streamplot` accepts a
``cmap`` argument that activates log-colouring of surface velocity streamlines
according to the velocity magnitude:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='w')
       ds.hyoga.plot.surface_velocity_streamplot(
           cmap='Blues', vmin=1e1, vmax=1e3, density=(6, 4))

   # needed to avoid distortion
   plt.gca().set_aspect('equal')

Composite plots
---------------

Combining major and minor contour levels at different intervals can be achieved
with a single call to :meth:`.Dataset.hyoga.plot.surface_altitude_contours`:

.. plot::

   with hyoga.open.example('pism.alps.out.2d.nc') as ds:
       ds.hyoga.plot.bedrock_altitude(center=False)
       ds.hyoga.plot.ice_margin(facecolor='w')
       ds.hyoga.plot.surface_altitude_contours(major=500, minor=100)

   # needed to avoid distortion
   plt.gca().set_aspect('equal')

More advanced composite examples are available in the :doc:`/examples/index`.
Here is one that uses :meth:`.Dataset.hyoga.assign_isostasy` and
:meth:`.Dataset.hyoga.plot.bedrock_isostasy` to compute and visualize
lithospheric deformation due to the load of the Alpine ice sheet during the
Last Glacial Maximum.

.. plot:: ../examples/datasets/plot_bedrock_isostasy.py

.. _cartopy: https://scitools.org.uk/cartopy/
.. _matplotlib: https://matplotlib.org
.. _xarray: https//xarray.pydata.org
