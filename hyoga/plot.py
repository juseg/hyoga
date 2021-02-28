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

    def bedrock_altitude(self, sealevel=0, cmap='Greys', zorder=-1, **kwargs):
        """Plot bedrock topography and shoreline."""
        var = self._ds.hyoga.getvar('bedrock_altitude') - sealevel
        var.plot.imshow(
            zorder=zorder, cmap=cmap, **kwargs)

    def bedrock_erosion(
            self, alpha=0.75, cmap='YlOrBr', constant=5.2e-8, exponent=2.34,
            **kwargs):
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
        **kwargs:
            Additional keyword arguments are passed to
            :meth:`matplotlib.axes.Axes.contourf`.

        Returns
        -------
        contours : QuadContourSet
            The resulting matplotlib contour set.
        """
        var = self._ds.hyoga.getvar('magnitude_of_land_ice_basal_velocity')
        var = (constant*var**exponent).assign_attrs(
            long_name='glacier erosion rate', units='mm a-1')
        return var.plot.contourf(alpha=alpha, cmap=cmap, **kwargs)

    def bedrock_isostasy(self, ax=None, alpha=0.75, cmap='PRGn_r', **kwargs):
        """Plot bedrock deformation contours."""
        var = self._ds.hyoga.getvar(
            'bedrock_altitude_change_due_to_isostatic_adjustment')

        # locate maximum depression (xarray has no idxmin yet)
        ax = ax or plt.gca()
        i, j = divmod(int(var.argmin()), var.shape[1])
        maxdep = float(-var[i, j])
        color = 'w' if maxdep > 50 else 'k'
        ax.plot(var.x[j], var.y[i], 'o', color=color, alpha=0.75)
        ax.annotate(
            '{:.0f} m'.format(maxdep), color=color, xy=(var.x[j], var.y[i]),
            xytext=(3, 3), textcoords='offset points')

        # plot bedrock deformation contours
        return var.plot.contourf(ax=ax, alpha=alpha, cmap=cmap, **kwargs)

    def bedrock_shoreline(
            self, sealevel=0, colors='0.25', linewidths=0.25, zorder=0,
            **kwargs):
        """Plot bedrock topography and shoreline."""
        var = self._ds.hyoga.getvar('bedrock_altitude') - sealevel
        var.plot.contour(
            colors=colors, levels=[0], linewidths=linewidths, zorder=zorder,
            **kwargs)

    def ice_margin(
            self, edgecolor='0.25', facecolor=None, linewidths=0.25, **kwargs):
        """Plot ice margin line and/or filled contour."""
        # FIXME make variable customizable
        var = self._ds.hyoga.getvar('land_ice_thickness')
        contours = []
        if edgecolor is not None:
            contours.append(var.notnull().plot.contour(
                colors=edgecolor, levels=[0.5], linewidths=linewidths,
                **kwargs))
        if facecolor is not None:
            contours.append(var.notnull().plot.contourf(
                colors=facecolor, extend='neither', levels=[0.5, 1.5],
                **kwargs))
        return contours if len(contours) > 1 else contours[0]

    def surface_altitude_contours(
            self, major=1000, minor=200, major_lw=0.25, minor_lw=0.1,
            **kwargs):
        """Plot minor and major surface topography contours."""
        # FIXME allow minor=None
        var = self._ds.hyoga.getvar('surface_altitude')
        levels = range(0, 5001, minor)
        return (
            var.plot.contour(
                levels=[lev for lev in levels if lev % major == 0],
                colors=['0.25'], linewidths=major_lw, **kwargs),
            var.plot.contour(
                levels=[lev for lev in levels if lev % major != 0],
                colors=['0.25'], linewidths=minor_lw, **kwargs))

    def surface_velocity(self, alpha=0.75, cmap='Blues', norm=None, **kwargs):
        """Plot surface velocity map."""
        norm = norm or mcolors.LogNorm()
        var = self._ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity')
        return var.plot.imshow(alpha=alpha, cmap=cmap, norm=norm, **kwargs)

    def surface_velocity_streamplot(
            self, ax=None, cmap='Blues', norm=None, arrowsize=0.25,
            linewidth=0.5, vmin=None, vmax=None, **kwargs):
        """Plot surface velocity streamlines."""

        # get axes, norm, data
        ax = ax or plt.gca()
        norm = norm or mcolors.LogNorm(vmin=vmin, vmax=vmax)
        uvar = self._ds.hyoga.getvar('land_ice_surface_x_velocity')
        vvar = self._ds.hyoga.getvar('land_ice_surface_y_velocity')

        # streamplot surface velocity
        try:
            return ax.streamplot(
                uvar.x, uvar.y, uvar.to_masked_array(), vvar.to_masked_array(),
                color=((uvar**2+vvar**2)**0.5).to_masked_array(), cmap=cmap,
                norm=norm, arrowsize=arrowsize, linewidth=linewidth, **kwargs)

        # streamplot colormapping fails on empty arrays (mpl issue #19323)
        except ValueError:
            return None
