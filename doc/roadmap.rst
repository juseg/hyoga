.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

:orphan:

Roadmap
=======

.. |x| raw:: html

    <input type="checkbox" disabled="" checked="">&nbsp;

.. |-| raw:: html

    <input type="checkbox" disabled="">&nbsp;

.. role:: depr(code)

v0.5.x Jobs
-----------

- |-| :class:`Job`
- |-| :class:`JobChain`?
- |-| :class:`JobFrame`?
- |-| doc: ``workflow/preparing``
- |-| doc: ``workflow/submitting``

v0.4.x Domains
--------------

- |-| :class:`.Domain`
- |-| :class:`.DomainSet`
- |-| doc: ``foreword/install``
- |-| doc: ``workflow/domains``

v0.3.x Inputs
-------------

- |-| :func:`hyoga.open.atmosphere`
- |-| :func:`hyoga.open.surface`
- |-| :func:`hyoga.open.timeseries`

v0.2.x Cartography
------------------

Datasets
~~~~~~~~

- |-| :meth:`.Dataset.hyoga.profile`
- |-| :meth:`.Dataset.hyoga.plot.barscale`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_hillshade`
- |x| :meth:`.Dataset.hyoga.plot.surface_hillshade`
- |x| :meth:`.Dataset.hyoga.plot.naturalearth`
- |x| :meth:`.Dataset.hyoga.plot.paleoglaciers`

Input
~~~~~

- |x| :func:`hyoga.open.naturalearth`
- |x| :func:`hyoga.open.paleoglaciers`

Documentation
~~~~~~~~~~~~~

- |x| :doc:`foreword/startup`
- |-| doc: ``foreword/history``
- |-| :doc:`datasets/shading`
- |-| :doc:`datasets/vectors`
- |-| doc: ``datasets/profile``

v0.1.x Plotting
---------------

Configuration
~~~~~~~~~~~~~

- |x| :obj:`hyoga.config`

Datasets
~~~~~~~~

- |x| :meth:`.Dataset.hyoga.assign_icemask`
- |x| :meth:`.Dataset.hyoga.assign_isostasy`
- |x| :meth:`.Dataset.hyoga.assign`
- |x| :meth:`.Dataset.hyoga.getvar`
- |x| :meth:`.Dataset.hyoga.interp`
- |x| :meth:`.Dataset.hyoga.where_icemask`
- |x| :meth:`.Dataset.hyoga.where_thicker`
- |x| :meth:`.Dataset.hyoga.where`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_altitude_contours`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_altitude`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_erosion`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_isostasy`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_shoreline`
- |x| :meth:`.Dataset.hyoga.plot.ice_margin`
- |x| :meth:`.Dataset.hyoga.plot.surface_altitude_contours`
- |x| :meth:`.Dataset.hyoga.plot.surface_velocity_streamplot`
- |x| :meth:`.Dataset.hyoga.plot.surface_velocity`

Input
~~~~~

- |x| :func:`hyoga.open.example`, renamed in :ref:`v0.2.0`
- |x| :func:`hyoga.open.dataset`
- |x| :func:`hyoga.open.mfdataset`
- |x| :func:`hyoga.open.subdataset`
- |x| :depr:`hyoga.open.visual`, deprecated in :ref:`v0.1.0`

Documentation
~~~~~~~~~~~~~

- |x| :doc:`datasets/plotting`
- |x| :doc:`datasets/opening`
- |x| :doc:`datasets/masking`
- |x| :doc:`examples/index`
- |x| :doc:`api/index`
- |x| :doc:`whatsnew`
