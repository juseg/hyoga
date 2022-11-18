.. Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Hyoga
=====

Hyoga is a small Python_ library to visualize ice-sheet model datasets.
It acts as a thin wrapper around GeoPandas_ and xarray_ for CF_-compliant
datasets on regular grids used for instance in PISM_. Hyoga (氷河) is the
Japanese word for glacier (lit. ice river).

.. _GeoPandas: https://geopandas.org
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

.. toctree::
   :caption: User guide
   :hidden:
   :maxdepth: 2

   foreword/startup
   datasets/index
   examples/index

.. toctree::
   :caption: Reference
   :hidden:
   :maxdepth: 2

   api/index
   roadmap
   whatsnew

.. admonition:: Citing

   Every hyoga release is long-term archived in Zenodo_ and attributed a DOI.
   This badge always indicates the latest record: |doi|.

.. |doi| image:: https://zenodo.org/badge/227465038.svg
   :target: https://zenodo.org/badge/latestdoi/227465038

.. this link always points to the latest record, too
.. _Zenodo: https://zenodo.org/record/4570420
