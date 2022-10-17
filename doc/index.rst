.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Hyoga
=====

Hyoga is a small Python_ library to visualize ice-sheet model datasets.
It acts as a thin wrapper around cartopy_ and xarray_ for CF_-compliant
datasets on regular grids used for instance in PISM_. Hyoga (氷河) is the
Japanese word for glacier (lit. ice river).

.. _cartopy: https://scitools.org.uk/cartopy/
.. _CF: https://cfconventions.org
.. _PISM: https://pism.io
.. _Python: https://python.org
.. _xarray: https://xarray.pydata.org/en/stable/

Since April 2022, development has been funded by a Trond Mohn Foundation (TMS_)
research project_ on alpine biodiversity at the University of Bergen (UiB_).

.. _TMS: https://mohnfoundation.no/en/
.. _UiB: https://www.uib.no/en
.. _project: mountainsinmotion.w.uib.no

.. raw:: html

   <figure>
     <div style="padding:56.25% 0 0 0;position:relative;">
       <iframe src="https://player.vimeo.com/video/321913054?h=c841d020b5&title=0&byline=0&portrait=0" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
     </div>
     <script src="https://player.vimeo.com/api/player.js"></script>
     <figcaption>
       <p>Example paleoglacier visualization made with hyoga.</p>
     </figcaption>
   </figure>

Documentation
-------------

.. toctree::
   :caption: User guide
   :maxdepth: 1

   foreword/startup
   datasets/opening
   datasets/plotting
   datasets/altitude
   datasets/vectors
   datasets/masking
   examples/index

.. toctree::
   :caption: Reference
   :maxdepth: 1

   api/index
   whatsnew

Get in touch
------------

At this point I am quite likely to follow my own development roadmap rather
than external suggestions. Still, if you are using hyoga, please feel free to
report bugs on Github_, and to get in touch with suggestions per email_.

.. _email: https://juseg.github.io
.. _Github: https://github.com/juseg/hyoga/
.. _Pypi: https://pypi.org/project/hyoga/

.. note::

   Hyoga is being developed on an entirely voluntary basis. I will be looking
   for funds to support my living. However, I have no prior experience with
   funding such open-source scientific software, and thus any suggestion or
   help will be greatly appreciated.

History
-------

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
:doc:`written <whatsnew>`.

.. _cartopy: https://scitools.org.uk/cartopy/
.. _dask: https://dask.org/
.. _iceplotlib: https://github.com/juseg/iceplotlib/
.. _pandas: https://pandas.pydata.org

Citing
------

Every hyoga release of is long-term archived in Zenodo_ and attributed a DOI.
This badge always indicates the latest record: |doi|.

.. |doi| image:: https://zenodo.org/badge/227465038.svg
   :target: https://zenodo.org/badge/latestdoi/227465038

.. this link always points to the latest record, too
.. _Zenodo: https://zenodo.org/record/4570420

License
-------

Hyoga is available under the `GNU General Public License v3.0+`__.

__ https://www.gnu.org/licenses/gpl-3.0.txt
