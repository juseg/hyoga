.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

:orphan:

History
=======

The idea for an object-oriented ice-sheet-model plotting library came in 2013.
At that time, I began developing an extension of the python-netcdf4 ``Dataset``
class in a little Python 2 package called iceplotlib_, which has been used by
some of my co-workers. But soon the little work I had done became very, very
largely outpaced by the powerful new additions to the Python geoscience
ecosystem cartopy_, pandas_, dask_, and xarray_.

In late 2019 as I began looking for a new academic position, a new library
building on these tools imposed itself as the evident technical ground for
future work. But proposals were rejected and I abandoned the idea again for
several months. Hyoga's first version was released on March 1st, 2021, exactly
one year after my last position ended. The rest of the story is yet to be
:doc:`written </whatsnew>`.

.. _cartopy: https://scitools.org.uk/cartopy/
.. _dask: https://dask.org/
.. _iceplotlib: https://github.com/juseg/iceplotlib/
.. _pandas: https://pandas.pydata.org
.. _xarray: https://xarray.pydata.org/en/stable/
