# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module extends the xarray plotting interface with convenience methods to
visualize ice sheet model output datasets. It is not meant to become an
exhaustive list of all possible visualizations, but rather to provide a few
shortcuts to oft-used plot methods with sensible defaults.
"""

import warnings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import hyoga.plot.colormaps
import hyoga.plot.hillshade
import hyoga.plot.scalebar


class HyogaPlotMethods:
    """
    A namespace to keep all plot methods in one place.
    """

    def __init__(self, accessor):
        self._hyoga = accessor
        self._ds = accessor._ds

    # Data array wrappers
    # -------------------

    def _contour(self, var, **kwargs):
        """Plot variable line contours with equal aspect and hidden axes."""
        cts = var.plot.contour(**kwargs)
        self._tailor_map_axes(cts.axes)
        return cts

    def _contourf(self, var, **kwargs):
        """Plot variable filled contours with equal aspect and hidden axes."""
        cts = var.plot.contourf(**kwargs)
        self._tailor_map_axes(cts.axes)
        return cts

    def _hillshade(self, var, altitude=None, azimuth=None, weight=None,
                   **kwargs):
        """Plot topographic variable multidirectional hillshade image."""
        var = hyoga.plot.hillshade._compute_multishade(
            var, altitude, azimuth, weight)
        style = dict(add_colorbar=False, cmap='Glossy')
        style.update(**kwargs)  # Py>=3.9: kwargs = defaults | kwargs
        return self._imshow(var, **style)

    def _imshow(self, var, **kwargs):
        """Plot variable image with equal aspect and hidden axes."""
        img = var.plot.imshow(**kwargs)
        self._tailor_map_axes(img.axes)
        return img

    def _streamplot(self, *args, **kwargs):
        """Plot streamplot with equal aspect and hidden axes."""
        # streamplot colormapping fails on empty arrays (mpl issue #19323)
        # (this is fixed in matplotlib 3.6.0, released Sep. 2022)
        ax = kwargs.pop('ax', plt.gca())
        try:
            streams = ax.streamplot(*args, **kwargs)
        except ValueError:
            streams = None
        self._tailor_map_axes(ax)
        return streams

    def _tailor_map_axes(self, ax):
        """Set aspect equal and hide axes and labels."""
        ax.set_aspect('equal')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    # Dataset plot methods
    # --------------------

    def bedrock_altitude(self, sealevel=0, **kwargs):
        """Plot bedrock topography and shoreline.

        Parameters
        ----------
        sealevel: float, optional
            Substract this value to the bedrock altitude before plotting. This
            will effectively shift the bedrock color mapping according to sea
            level, which may be useful for instance if different colors are
            used for negative and positive elevations. Note that `vmax=3000`,
            though, will always be 3000 bedrock altitude units above sea level.

            .. deprecated:: 0.2.1
                will be removed in version 0.4.0. To center the colormap around
                sealevel, use the xarray keyword argument ``center=sealevel``.

        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
            Defaults to a grey colormap, `zorder=-1` so that any other plot
            becomes an overlay to the bedrock altitude, and disabling the
            xarray colorbar.

        Returns
        -------
        image: AxesImage
            The plotted bedrock altitude image.
        """
        style = dict(add_colorbar=False, cmap='Greys', zorder=-1)
        style.update(kwargs)
        # if threshold is present, compute an ice mask
        if sealevel != 0:
            warnings.warn(
                "the sealevel argument is deprecated and will be removed in "
                "v0.4.0, use center=sealevel instead.", FutureWarning)
        var = self._hyoga.getvar('bedrock_altitude') - sealevel
        return self._imshow(var, **style)

    def bedrock_altitude_contours(self, **kwargs):
        """Plot bedrock topography filled countours.

        Parameters
        ----------
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contourf`.
            If any of ``Topographic``, ``Bathymetric``, or ``Elevational`` is
            passed as ``cmap``, and both ``colors`` and ``levels`` are missing,
            they will use a predefined set enhancing detail near the zero. The
            altitude range remains adjustable using ``vmin`` and ``vmax``.
            Defaults to a grey colormap, ``zorder=-1`` so that any other plot
            becomes an overlay to the bedrock altitude.

        Returns
        -------
        contours : QuadContourSet
            The plotted bedrock altitude contour set.
        """

        # get plotting style, read bedrock altitude
        style = dict(add_colorbar=True, cmap='Greys', zorder=-1)
        style.update(kwargs)
        darray = self._hyoga.getvar('bedrock_altitude')

        # if hyoga altitude colormap was passed but no colors or levels
        if style['cmap'] in ['Topographic', 'Bathymetric', 'Elevational'] and \
                not any(('colors' in style, 'levels' in style)):

            # replace colormap by color list
            tuples = hyoga.plot.colormaps.SEQUENCES[style.pop('cmap')]
            tuples = list(dict(tuples).items())  # remove Elevational dup level
            colors = [t[1] for t in tuples]  # could use dict.values()
            colors = colors + [colors[-1]]

            # get vmin, vmax or rounded data bounds from matplotlib ticker
            bounds = darray.min(), darray.max()
            bounds = mpl.ticker.MaxNLocator().tick_values(*bounds)[[0, -1]]
            vmin = style.pop('vmin', bounds[0])
            vmax = style.pop('vmax', bounds[1])

            # normalize levels from 0-1 to data bounds
            levels = [t[0] for t in tuples]  # could use dict.keys()
            levels = [vmin+(vmax-vmin)*lev for lev in levels]

            # update plotting style keyword arguments
            style.update(colors=colors, levels=levels)

            # passing a BoundaryNorm resets the cmap yielding misplaced colors
            # style['cmap'], style['norm'] = mpl.colors.from_levels_and_colors(
            #         levels, colors[:-1], extend='min')

        # plot and return contour set
        return self._contourf(darray, **style)

    def bedrock_erosion(self, constant=5.2e-8, exponent=2.34, **kwargs):
        """Plot erosion rate based on basal velocity.

        Parameters
        ----------
        constant: float, optional
            Constant in the erosion law, in units of ``1e-3 m^(1-l) a^(l-1)``
            where ``l`` corresponds to the exponent. Published values include
            ``1.665e-1`` (Cook et al., 2020), ``2.7e-4`` (Herman et al., 2015),
            ``1e-1`` (Humphrey and Raymond, 1994), and the default ``5.2e-8``
            (Koppes et al., 2015).
        exponent: float, optional
            Exponent in the erosion law, unitless. Published values include
            ``0.6459`` (Cook et al., 2020), ``2.02`` (Herman et al., 2015),
            ``1`` (Humphrey and Raymond, 1994), and the default ``2.34``
            (Koppes et al., 2015).
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contourf`.
            Defaults to a brownish colormap and light transparency.

        Returns
        -------
        contours : QuadContourSet
            The plotted bedrock erosion contour set.
        """
        # NOTE locator=mpl.ticker.LogLocator() seem to have no effect?
        style = dict(alpha=0.75, cmap='YlOrBr')
        style.update(kwargs)
        var = self._hyoga.getvar('magnitude_of_land_ice_basal_velocity')
        var = var.where(self._hyoga.getvar('land_ice_area_fraction') >= 0.5)
        var = (constant*var**exponent).assign_attrs(
            long_name='glacier erosion rate', units='mm a-1')
        return self._contourf(var, **style)

    def bedrock_hillshade(self, altitude=None, azimuth=None, weight=None,
                          exag=1, **kwargs):
        """Plot bedrock altitude multidirectional hillshade.

        Parameters
        ----------
        altitude: float or iterable, optional
            Altitude angle(s) of illumination in degrees. Defaults to three
            light sources at 45 degrees. Any of ``azimuth``, ``altitude`` and
            ``weight`` provided as iterables need to have equal lengths.
        azimuth: float or iterable, optional
            Azimuth angle(s) of illumination in degrees (clockwise from north).
            Defaults to three light sources at 255, 315 and 15 degree azimuths.
        weight: float or iterable, optional
            Weight coefficient(s) for each unidirectional hillshade array. It
            is intended, but not required, that the weights add up to 1.
            Defaults to [0.25, 0.5, 0.25].
        exag: float, optional
            Altitude exaggeration factor, defaults to 1.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
            Defaults to a glossy colormap.

        Returns
        -------
        image: AxesImage
            The plotted bedrock hillshade image.
        """
        darray = self._hyoga.getvar('bedrock_altitude') * exag
        return self._hillshade(
            darray, altitude=altitude, azimuth=azimuth, weight=weight,
            **kwargs)

    def bedrock_isostasy(self, **kwargs):
        """Plot bedrock deformation contours and locate minumum.

        Parameters
        ----------
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contourf`.
            Defaults to a purple-green colormap and light transparency.

        Returns
        -------
        contours : QuadContourSet
            The plotted bedrock isostasy contour set.
        """

        # get bedrock isostasy variable
        var = self._hyoga.getvar(
            'bedrock_altitude_change_due_to_isostatic_adjustment')

        # locate maximum depression (xarray has no idxmin yet)
        ax = kwargs.get('ax', plt.gca())
        i, j = divmod(int(var.argmin()), var.shape[1])
        maxdep = float(-var[i, j])
        color = 'w' if maxdep > 50 else 'k'
        ax.plot(var.x[j], var.y[i], 'o', color=color, alpha=0.75)
        ax.annotate(
            f'{maxdep:.0f} m', color=color, xy=(var.x[j], var.y[i]),
            xytext=(3, 3), textcoords='offset points')

        # plot bedrock deformation contours
        style = dict(alpha=0.75, cmap='PRGn_r')
        style.update(**kwargs)
        return self._contourf(var, **style)

    def bedrock_shoreline(self, sealevel=0, **kwargs):
        """Plot bedrock shoreline contour.

        Parameters
        ----------
        sealevel: float, optional
            A single contour level determining the shoreline altitude. Will be
            overriden if ``levels`` is present in ``kwargs``.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contour`.
            Defaults to a dark gray thin contour.

        Returns
        -------
        contours : QuadContourSet
            The plotted bedrock shoreline contour set.
        """
        style = dict(colors=['0.25'], levels=[sealevel], linewidths=0.25)
        style.update(**kwargs)
        var = self._hyoga.getvar('bedrock_altitude')
        return self._contour(var, **style)

    def ice_margin(self, edgecolor='0.25', facecolor=None, **kwargs):
        """Plot ice margin line and/or filled contour

        Parameters
        ----------
        edgecolor: matplotlib color, optional
            Color for the ice margin contour line, defaults to dark grey.
        facecolor: matplotlib color, optional
            Color for the glacierized area fill, defaults to none.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contour`
            and :meth:`xarray.DataArray.plot.contourf`. Defaults to a thin
            contour line for the ice margin and no fill. If ``facecolor`` is
            provided, defaults to applying light transparency in the fill.

        Returns
        -------
        contours : QuadContourSet
            The plotted ice margin contour set or a tuple of two contour sets
            if both `edgecolor` and `facecolor` were given.
        """
        var = self._hyoga.getvar('land_ice_area_fraction')
        contours = []
        if edgecolor is not None:
            style = dict(colors=[edgecolor], levels=[0.5], linewidths=0.25)
            style.update(kwargs)
            contours.append(self._contour(var, **style))
        if facecolor is not None:
            style = dict(add_colorbar=False, alpha=0.75, colors=[facecolor],
                         extend='neither', levels=[0.5, 1.5])
            style.update(kwargs)
            contours.append(self._contourf(var, **style))
        return contours if len(contours) > 1 else contours[0]

    def surface_altitude_contours(self, major=1000, minor=200, **kwargs):
        """Plot minor and major surface topography contours.

        Parameters
        ----------
        major: float, optional
            Contour interval between major elevation contours.
        minor: float, optional
            Contour interval between minor elevation contours.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contour`.
            Defaults to dark gray thin line for major elevation contours, and
            even thinner line for minor contours.

        Returns
        -------
        contours : QuadContourSet
            The plotted ice margin contour set or a tuple of two contour sets
            if both `major` and `minor` were given (as in the default case).
        """
        var = self._hyoga.getvar('surface_altitude')
        var = var.where(self._hyoga.getvar('land_ice_area_fraction') >= 0.5)
        levels = range(0, 5001, minor)
        contours = []
        if major is not None:
            style = dict(colors=['0.25'], linewidths=0.25)
            style.update(kwargs)
            contours.append(self._contour(
                var,
                levels=[lev for lev in levels if lev % major == 0], **style))
        if minor is not None:
            style = dict(colors=['0.25'], linewidths=0.1)
            style.update(kwargs)
            contours.append(self._contour(
                var,
                levels=[lev for lev in levels if lev % major != 0], **style))
        return contours if len(contours) > 1 else contours[0]

    def surface_hillshade(self, altitude=None, azimuth=None, weight=None,
                          exag=1, **kwargs):
        """Plot surface altitude multidirectional hillshade.

        Parameters
        ----------
        altitude: float or iterable, optional
            Altitude angle(s) of illumination in degrees. Defaults to three
            light sources at 45 degrees. Any of ``azimuth``, ``altitude`` and
            ``weight`` provided as iterables need to have equal lengths.
        azimuth: float or iterable, optional
            Azimuth angle(s) of illumination in degrees (clockwise from north).
            Defaults to three light sources at 255, 315 and 15 degree azimuths.
        weight: float or iterable, optional
            Weight coefficient(s) for each unidirectional hillshade array. It
            is intended, but not required, that the weights add up to 1.
            Defaults to [0.25, 0.5, 0.25].
        exag: float, optional
            Altitude exaggeration factor, defaults to 1.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
            Defaults to a glossy colormap.

        Returns
        -------
        image: AxesImage
            The plotted surface hillshade image.
        """
        darray = self._hyoga.getvar('surface_altitude') * exag
        return self._hillshade(
            darray, altitude=altitude, azimuth=azimuth, weight=weight,
            **kwargs)

    def surface_velocity(self, **kwargs):
        """Plot surface velocity map.

        Parameters
        ----------
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.imshow`.
            Defaults to a blue colormap, light transparency, and logarithmic
            scaling, whose limits can be adjusted using ``vmin`` and ``vmax``.

        Returns
        -------
        image: AxesImage
            The plotted surface velocity image.
        """
        style = dict(alpha=0.75, cmap='Blues', norm=mpl.colors.LogNorm())
        style.update(kwargs)
        var = self._hyoga.getvar('magnitude_of_land_ice_surface_velocity')
        var = var.where(self._hyoga.getvar('land_ice_area_fraction') >= 0.5)
        return self._imshow(var, **style)

    def surface_velocity_streamplot(self, **kwargs):
        """Plot surface velocity streamlines.

        Parameters
        ----------
        **kwargs: optional
            Keyword arguments passed to :meth:`matplotlib.Axes.streamplot`.
            Defaults to a blue colormap and logarithmic scaling, whose limits
            can be adjusted using ``vmin`` and ``vmax``. Note that the
            ``density`` keyword can greaty affect plotting speed. If the domain
            plotted is not square, you may also want to set ``density`` as a
            tuple proportional to the axes aspect ratio.

        Returns
        -------
        streamlines: StreamplotSet
            The plotted surface velocity streamlines.
        """

        # IDEA: add basal streamplot mostly sharing this code

        # get style parameters
        vmin = kwargs.pop('vmin', None)  # not a streamplot param
        vmax = kwargs.pop('vmax', None)  # not a streamplot param
        norm = kwargs.get('norm', mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
        style = dict(arrowsize=0.25, cmap='Blues', linewidth=0.5)
        style.update(kwargs)

        # get velocity component variables
        mask = self._hyoga.getvar('land_ice_area_fraction') >= 0.5
        uvar = self._hyoga.getvar('land_ice_surface_x_velocity').where(mask)
        vvar = self._hyoga.getvar('land_ice_surface_y_velocity').where(mask)
        cvar = (uvar**2+vvar**2)**0.5

        # streamplot surface velocity
        return self._streamplot(
                uvar.x.data, uvar.y.data, uvar.data, vvar.data,
                color=cvar.to_masked_array(), norm=norm, **style)

    # Vector plot methods
    # -------------------

    def natural_earth(
            self, theme=None, category='physical', scale='10m', **kwargs):
        """Plot Natural Earth data in dataset projection.

        Parameters
        ----------
        theme : str or iterable, optional
            Natural Earth data theme(s) or theme aliase(s), such as ``rivers``
            or ``lakes_all`` passed to :func:`hyoga.open.natural_earth`. If
            theme is None, plot coastline, rivers and lakes. Please browse
            https://www.naturalearthdata.com for available themes.
        category : {'cultural', 'physical'}, optional
            Natural Earth data category (i.e. folder) used for downloads,
            defaults to 'physical'.
        scale : {'10m', '50m', '110m'}, optional
            Natural Earth data scale controlling the level of detail, defaults
            to the highest scale of 10m.
        **kwargs: optional
            Keyword arguments passed to :meth:`geopandas.GeoDataFrame.plot`.
            Defaults to plotting on current axes at ``zorder=-1``, the same
            level as bedrock altitude maps. If theme is None, also apply a
            default style to coastline, rivers, and lakes.

        Returns
        -------
        ax : :class:`matplotlib.axes.Axes` (or a subclass)
            Matplotlib axes used for plotting.
        """

        # if theme is None plot coastline, rivers and lakes
        # IDEA: apply default style on any individual theme
        if theme is None:
            edgecolor = kwargs.pop('edgecolor', '0.25')
            facecolor = kwargs.pop('facecolor', '0.95')
            linewidth = kwargs.pop('linewidth', 0.5)
            ax = self.natural_earth(
                'coastline', edgecolor=edgecolor, linestyle='dashed',
                linewidth=linewidth/2, **kwargs)
            ax = self.natural_earth(
                'rivers_all', edgecolor=edgecolor, linewidth=linewidth,
                **kwargs)
            ax = self.natural_earth(
                'lakes_all', edgecolor=edgecolor, facecolor=facecolor,
                linewidth=linewidth/2, **kwargs)
            return ax

        # default to plotting on current axes background
        kwargs.setdefault('ax', plt.gca())
        kwargs.setdefault('zorder', -1)

        # prevent autoscaling (this is not ideal)
        # TODO: open geopandas issue to allow gdf.plot(autolim=False)
        kwargs['ax'].set_autoscale_on(False)

        # get dataset crs (or proj4 attr for backward compat)
        crs = self._ds.rio.crs or self._ds.proj4

        # open natural earth data, reproject and plot
        gdf = hyoga.open.natural_earth(theme, category=category, scale=scale)
        return gdf.to_crs(crs).plot(**kwargs)

    def paleoglaciers(self, source='ehl11', **kwargs):
        """Plot Last Glacial Maximum paleoglacier extent.

        Parameters
        ----------
        source : 'ehl11' or 'bat19'
            Source of paleoglacier extent data, either Ehlers et al. (2011) or
            Batchelor et al. (2019).
        **kwargs: optional
            Keyword arguments passed to :meth:`geopandas.GeoDataFrame.plot`.
            Defaults to plotting on current axes at ``zorder=-1``, the same
            level as bedrock altitude maps.

        Returns
        -------
        ax : :class:`matplotlib.axes.Axes` (or a subclass)
            Matplotlib axes used for plotting.
        """

        # default to plotting on current axes background
        kwargs.setdefault('ax', plt.gca())
        kwargs.setdefault('zorder', -1)

        # prevent autoscaling (this is not ideal)
        # TODO: open geopandas issue to allow gdf.plot(autolim=False)
        kwargs['ax'].set_autoscale_on(False)

        # get dataset crs (or proj4 attr for backward compat)
        crs = self._ds.rio.crs or self._ds.proj4

        # open paleoglaciers data, reproject and plot
        gdf = hyoga.open.paleoglaciers(source=source)
        return gdf.to_crs(crs).plot(**kwargs)

    # Axes decorations
    # ----------------

    def scale_bar(
            self, ax=None, label=None, loc='lower right', size=None, **kwargs):
        """Add a horizontal bar with a text label showing map scale.

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes` (or a subclass), optional
            Matplotlib axes used for plotting. Default to current axes.
        label : str, optional
            Text label. If None provided, assume coordinates are in meters, and
            add label in kilometers according to the size parameter.
        loc : str, optional
            Location of the scale bar relative to axes (e.g. 'upper left',
            'center right'), default to 'lower right'. See the `loc` parameter
            of :class:`matplotlib.axes.Axes.legend` for details.
        size : float, optional
            Bar size in data coordinates. Default to a function of axes area
            rounded on an approximate log scale (1, 2, 5, 10, 20 km etc).
        **kwargs : optional
            Additional keyword arguments are passed to the
            :class:`matplotlib.lines.Line2D` artist for the scale bar. Default
            to a black bar with a vertical marker on each end.

        Returns
        -------
        abs : :class:`~AnchoredScaleBar`
            An anchored container for the scale bar and text label.
        """

        # get current axes if None provided
        if ax is None:
            ax = plt.gca()

        # size defaults to a function of axes extent
        if size is None:
            # compute axes area
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            area = (xlim[1]-xlim[0])**2 + (ylim[1]-ylim[0])**2
            # divide square root of area by ten
            size = float(area)**0.5 / 10
            # round log10 to nearest increment
            log = round(3*np.log10(size)) / 3
            # approximate to first significant figure
            size = round(10**log, -int(log))

        # by default assume the unit is meters
        # IDEA: use x and y unit attribute instead
        if label is None:
            label = f'{size/1e3:.0f}' + r'$\,$km'

        # init scale bar
        style = dict(color='black', marker='|')
        style.update(kwargs)
        asb = hyoga.plot.scalebar.AnchoredScaleBar(
            label=label, loc=loc, size=size, transform=ax.transData, **style)

        # add scale bar to axes
        return ax.add_artist(asb)
