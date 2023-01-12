.. Copyright (c) 2022, Julien Seguinot (juseg.github.io)
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Development roadmap
===================

My long-term goal for hyoga is to develop a fully automated workflow to model
paleoglaciers with PISM, and perhaps other models, anywhere on Earth.

I hope that hyoga will eventually become a community package. Yet for the time
being, the code base is still unstable, thus I will likely prioritise my own
development roadmap over user requests.

Until I come up with better contributing guidelines and co, here is an evolving
document that I use to keep track of my progress and plan future releases, some
kind of incremental version of the :doc:`api`, with a glimpse into the future.
I hope to release ``v0.5.0`` sometime in Spring 2023.

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

- |x| :func:`hyoga.open.atmosphere`
- |x| :func:`hyoga.open.bootstrap`
- |-| :func:`hyoga.open.timeseries`
- |x| :doc:`datasets/opening`

v0.2.x Cartography
------------------

Datasets
~~~~~~~~

- |x| :meth:`.Dataset.hyoga.profile`
- |x| :meth:`.Dataset.hyoga.plot.bedrock_hillshade`
- |x| :meth:`.Dataset.hyoga.plot.surface_hillshade`
- |x| :meth:`.Dataset.hyoga.plot.natural_earth`
- |x| :meth:`.Dataset.hyoga.plot.paleoglaciers`
- |x| :meth:`.Dataset.hyoga.plot.scale_bar`

Input
~~~~~

- |x| :func:`hyoga.open.natural_earth`
- |x| :func:`hyoga.open.paleoglaciers`

Documentation
~~~~~~~~~~~~~

- |x| :doc:`foreword/startup`
- |-| doc: ``foreword/history``
- |x| :doc:`datasets/shading`
- |x| :doc:`datasets/vectors`

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
- |x| :doc:`datasets/masking`, renamed in :ref:`v0.3.0`
- |x| :doc:`datasets/refining`, renamed in :ref:`v0.3.0`
- |x| :doc:`examples/index`
- |x| :doc:`api/index`
- |x| :doc:`whatsnew`
