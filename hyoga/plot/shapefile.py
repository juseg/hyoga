# Copyright (c) 2018-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module adds functions to plot shapefiles throught cartopy, but with some
improvements, such as added speed by ignoring shapes outside the axes extent,
highlighting particular shapes, and removing duplicates. These functions are
used internally to plot Natural Earth data and paleoglaciers.
"""

import matplotlib.pyplot as plt
import shapely.geometry
import cartopy


def shapefile(filename, ax=None, crs=None, subject=None, **kwargs):
    """Plot shapefile geometries intersecting axes extent.

    Parameters
    ----------
    filename : str, Path or file-like
        Path to a shapefile. Only intersecting geometries will be plotted. This
        may improve speed when plotting global data on small domains.
    ax : cartopy GeoAxes or subclass, optional
        Axes on which to plot, default to the current axes. Plotting will fail
        on non-:mod:`cartopy` axes.
    crs : cartopy CRS, optional
        Coordinate reference system used by shapefile, default to
        `cartopy.crs.PlateCarree`.
    subject : str, optional
        The ``name`` or ``NAME`` attribute of a record to be considered as the
        primary subject for plotting.
    **kwargs : optional
        Keyword arguments passed to
        :meth:`cartopy.mpl.geoaxes.GeoAxes.add_geometries`. Keyword argument
        prefixed with ``subject_`` (e.g. ``subject_facecolor``) will be passed
        to :meth:`cartopy.mpl.geoaxes.GeoAxes.add_geometries` when plotting the
        subject.

    Returns
    -------
    geometries : tuple
        A :class:`cartopy.mpl.feature_artist.FeatureArtist` instance or a tuple
        of (context, subject) feature artists if the subject is not ``None``.
    """

    # get current axes if None provided
    ax = ax or plt.gca()

    # prepare axes extent geometry
    crs = crs or cartopy.crs.PlateCarree()
    axes_box = _get_extent_geometry(ax=ax, crs=crs)

    # open shapefile data
    shp = cartopy.io.shapereader.Reader(filename)

    # separate context and subject kwargs
    subject_kw = {
        k[8:]: v for k, v in kwargs.items() if k.startswith('subject_')}
    context_kw = {
        k: v for k, v in kwargs.items() if not k.startswith('subject_')}

    # find intersecting geometries
    subject_geometries = []
    context_geometries = []
    for rec in shp.records():
        if rec.geometry is not None and axes_box.intersects(rec.geometry):
            name = rec.attributes.get('name', rec.attributes.get('NAME', None))
            if subject is not None and name == subject and \
                    rec.geometry not in subject_geometries:
                subject_geometries.append(rec.geometry)
            elif rec.geometry not in context_geometries:
                context_geometries.append(rec.geometry)

    # plot intersecting geometries
    if subject is None:
        return ax.add_geometries(context_geometries, crs, **context_kw)
    return (ax.add_geometries(context_geometries, crs, **context_kw),
            ax.add_geometries(subject_geometries, crs, **subject_kw))


def _get_extent_geometry(ax=None, crs=None):
    """Return axes extent as shapely geometry."""
    ax = ax or plt.gca()
    west, east, south, north = ax.get_extent(crs=crs)
    return shapely.geometry.box(west, south, east, north)
