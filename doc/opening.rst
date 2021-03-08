.. Copyright (c) 2021, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Reading model output
====================

Opening output files
--------------------

Let us open demo data. This will download a model output data file from the
web, and store it into a ``~/.cache/hyoga`` directory so that it can be reused
the next time.

.. ipython:: python

   import xarray as xr
   import hyoga.demo
   ds = xr.open_dataset(hyoga.demo.get('pism.alps.out.2d.nc'))

Alternatively, ``hyoga.open`` provides thin wrappers around xarray functions to
open a single-file dataset, a multi-file dataset, and a single time slice
within a multi-file dataset.

.. autosummary::
   :nosignatures:

   hyoga.open.dataset
   hyoga.open.mfdataset
   hyoga.open.subdataset

.. warning::
   These functions convert model time to an age coordinate in ka before the
   present. This functionality is not always useful and will be reworked in
   future versions using Climate and Forecast (CF) time conventions. If you do
   not need an age coordinate, please use regular :meth:`xarray.open_dataset`
   for the time being.

Selecting data
--------------

Please refer to the excellent xarray_ docs to explore the many other ways of
indexing and subsetting data. As long as hyoga (or any submodule) has been
imported, new functionality will be available in a so-called "dataset accessor"
attribute ``ds.hyoga``:

.. ipython:: python

   ds.hyoga

.. note::

   I am thinking about renaming ``ds.hyoga`` to ``ds.ice`` starting from
   v0.2.0. The name may be used in other projects though, I am not sure. In any
   case ``ds.hyoga`` would remain backward-compatible for a while. If you
   have an opinion about that, feel free to share it on Github (:issue:`13`).

In particular, hyoga never accesses model variables by their "short names".
While ``thk``, for instance refers to ice
thickness in PISM, it may refer to a different quantity, or to nothing at all,
in another ice-sheet model. This where `CF standard names`_ come into play. To
access a variable by standard name you may use:

.. ipython:: python

   var = ds.hyoga.getvar('land_ice_thickness');
   var.max()
   var.units

If a particular variable is missing, hyoga will additionally try to reconstruct
it from others, such as the sum of bedrock altitude and ice thickness for
surface altitude, or the norm of velocity components for its magnitude.  This
mechanism can be disable using ``infer=False`` when unwanted:

.. ipython:: python
   :okexcept:

   ds.hyoga.getvar('surface_altitude');
   ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity');
   ds.hyoga.getvar('surface_altitude', infer=False)

Because `CF standard names`_ for land ice variables are relatively recent,
older ice sheet models may not include them in output metadata. For PISM, a
mechanism has been implemented to fill (some of) these missing standard names
during initialization.

.. note::

   While hyoga has only been tested with PISM so far, it is my hope that it
   will become compatible with some other glacier and ice sheet models in the
   future. If you want to make your glacier model compatible with hyoga, please
   consider implementing `CF standard names`_.


Interpolation and masking
-------------------------

Hyoga already includes a few more tools meant to postprocess data before
plotting. Please refer to the programming interface for their documentation.

.. currentmodule:: xarray

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Dataset.hyoga.assign_isostasy
   Dataset.hyoga.getvar
   Dataset.hyoga.interp
   Dataset.hyoga.where
   Dataset.hyoga.where_thicker


.. _xarray: https//xarray.pydata.org
.. _`CF standard names`: http://cfconventions.org/standard-names.html
