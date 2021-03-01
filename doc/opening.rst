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
   ds = xr.open_dataset(hyoga.demo.pism_gridded())

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

The demo data is indexed by age in kiloyears (ka). Thanks to the power of
xarray, selecting an age-slice of the ice thickness is as easy as:

.. ipython:: python

   ds.sel(age=24).thk  # or ds.thk.sel(age=24)

Please refer to the excellent xarray_ to explore the many other ways of
indexing and subsetting data. As long as hyoga (or any submodule) has been
imported, new functionality will be available in a so-called "dataset accessor"
attribute ``ds.hyoga``:

.. ipython:: python

   ds.hyoga

In particular, hyoga never accesses model variables by their "short names" (e.g.
``thk``) as was done in the example above. While ``thk`` refers to ice
thickness in PISM, it may refer to a different quantity, or to nothing at all,
in another ice-sheet model. This where `CF standard names`_ come into play. To
access a variable by standard name you may use:

.. ipython:: python

   var = ds.hyoga.getvar('land_ice_thickness');
   var.max()
   var.units

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

.. autosummary::
   :nosignatures:

   hyoga.hyoga.HyogaDataset.assign_isostasy
   hyoga.hyoga.HyogaDataset.interp
   hyoga.hyoga.HyogaDataset.where
   hyoga.hyoga.HyogaDataset.where_thicker

.. _xarray: https//xarray.pydata.org
.. _`CF standard names`: http://cfconventions.org/standard-names.html
