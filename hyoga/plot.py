# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module extends the xarray plotting interface with convenience methods to
visualize ice sheet model output datasets. It is not meant to become an
exhaustive list of all possible visualizations, but rather to provide a few
shortcuts to oft-used plot methods with sensible defaults.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class HyogaPlotMethods:
    """
    A namespace to keep all plot methods in one place.
    """

    def __init__(self, dataset):
        self._ds = dataset

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
        var = self._ds.hyoga.getvar('bedrock_altitude') - sealevel
        return var.plot.imshow(**style)

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
        var = self._ds.hyoga.getvar('magnitude_of_land_ice_basal_velocity')
        var = (constant*var**exponent).assign_attrs(
            long_name='glacier erosion rate', units='mm a-1')
        return var.plot.contourf(**style)

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
        var = self._ds.hyoga.getvar(
            'bedrock_altitude_change_due_to_isostatic_adjustment')

        # locate maximum depression (xarray has no idxmin yet)
        ax = kwargs.get('ax', plt.gca())
        i, j = divmod(int(var.argmin()), var.shape[1])
        maxdep = float(-var[i, j])
        color = 'w' if maxdep > 50 else 'k'
        ax.plot(var.x[j], var.y[i], 'o', color=color, alpha=0.75)
        ax.annotate(
            '{:.0f} m'.format(maxdep), color=color, xy=(var.x[j], var.y[i]),
            xytext=(3, 3), textcoords='offset points')

        # plot bedrock deformation contours
        style = dict(alpha=0.75, cmap='PRGn_r')
        style.update(**kwargs)
        return var.plot.contourf(**style)

    def bedrock_shoreline(self, sealevel=0, **kwargs):
        """Plot bedrock topography and shoreline.

        Parameters
        ----------
        sealevel: float, optional
            Substract this value to the bedrock altitude before plotting. This
            will effectively shift the shoreline according to sea level.
        **kwargs: optional
            Keyword arguments passed to :meth:`xarray.DataArray.plot.contour`.
            Defaults to a dark gray thin contour.

        Returns
        -------
        contours : QuadContourSet
            The plotted bedrock shoreline contour set.
        """
        style = dict(colors=['0.25'], levels=[0], linewidths=0.25, zorder=0)
        style.update(**kwargs)
        var = self._ds.hyoga.getvar('bedrock_altitude') - sealevel
        return var.plot.contour(**style)

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
        # NOTE this method may use a mask variable in the future (#9)
        var = self._ds.hyoga.getvar('land_ice_thickness')
        contours = []
        if edgecolor is not None:
            style = dict(colors=[edgecolor], levels=[0.5], linewidths=0.25)
            style.update(kwargs)
            contours.append(var.notnull().plot.contour(**style))
        if facecolor is not None:
            style = dict(add_colorbar=False, alpha=0.75, colors=[facecolor],
                         extend='neither', levels=[0.5, 1.5])
            style.update(kwargs)
            contours.append(var.notnull().plot.contourf(**style))
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
        var = self._ds.hyoga.getvar('surface_altitude')
        levels = range(0, 5001, minor)
        contours = []
        if major is not None:
            style = dict(colors=['0.25'], linewidths=0.25)
            style.update(kwargs)
            contours.append(var.plot.contour(
                levels=[lev for lev in levels if lev % major == 0], **style))
        if minor is not None:
            style = dict(colors=['0.25'], linewidths=0.1)
            style.update(kwargs)
            contours.append(var.plot.contour(
                levels=[lev for lev in levels if lev % major != 0], **style))
        return contours if len(contours) > 1 else contours[0]

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
        style = dict(alpha=0.75, cmap='Blues', norm=mcolors.LogNorm())
        style.update(kwargs)
        var = self._ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity')
        return var.plot.imshow(**style)

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

        # get style parameters
        ax = kwargs.pop('ax', plt.gca())  # not a mpl kwargs
        vmin = kwargs.pop('vmin', None)  # not a streamplot param
        vmax = kwargs.pop('vmax', None)  # not a streamplot param
        norm = kwargs.get('norm', mcolors.LogNorm(vmin=vmin, vmax=vmax))
        style = dict(arrowsize=0.25, cmap='Blues', linewidth=0.5)
        style.update(kwargs)

        # get velocity component variables
        uvar = self._ds.hyoga.getvar('land_ice_surface_x_velocity')
        vvar = self._ds.hyoga.getvar('land_ice_surface_y_velocity')
        cvar = (uvar**2+vvar**2)**0.5

        # streamplot surface velocity
        try:
            return ax.streamplot(
                uvar.x, uvar.y, uvar.to_masked_array(), vvar.to_masked_array(),
                color=cvar.to_masked_array(), norm=norm, **style)

        # streamplot colormapping fails on empty arrays (mpl issue #19323)
        except ValueError:
            return None
