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

    def bedrock_altitude(self, ax=None, sealevel=0, style='grey'):
        """Plot bedrock topography and shoreline."""
        var = self._ds.hyoga.getvar('bedrock_altitude') - sealevel
        var.plot.imshow(
            ax=ax, add_colorbar=False, zorder=-1,
            cmap='Greys', vmin=0, vmax=4500)
        var.plot.contour(
            ax=ax, colors=('#0978ab' if style == 'wiki' else '0.25'),
            levels=[0], linestyles='dashed', linewidths=0.25, zorder=0)

    def bedrock_erosion(self, ax=None):
        """Plot erosion rate based on basal velocity."""
        ds = self._ds
        return (5.2e-8*ds.velbase_mag**2.34).plot.contourf(
                ax=ax, add_colorbar=False, alpha=0.75, cmap='YlOrBr',
                levels=[10**i for i in range(-9, 1)])

    def bedrock_isostasy(self, ax=None):
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
        return var.plot.contourf(
            ax=ax, add_colorbar=False, alpha=0.75, cmap='PRGn_r',
            levels=[-100, -50, -20, 0, 2, 5, 10])

    def ice_margin(self, ax=None, edgecolor='0.25', facecolor=None, **kwargs):
        """Plot ice margin line and/or filled contour."""
        # FIXME make variable customizable
        var = self._ds.hyoga.getvar('land_ice_thickness')
        contours = []
        if edgecolor is not None:
            contours.append(var.notnull().plot.contour(
                ax=ax, colors=edgecolor, levels=[0.5], linewidths=0.25,
                **kwargs))
        if facecolor is not None:
            contours.append(var.notnull().plot.contourf(
                ax=ax, add_colorbar=False, colors=facecolor, extend='neither',
                levels=[0.5, 1.5], **kwargs))
        return contours if len(contours) > 1 else contours[0]

    def surface_altitude_contours(self, ax=None, minor=200, major=1000):
        """Plot minor and major surface topography contours."""
        # FIXME allow minor=None
        var = self._ds.hyoga.getvar('surface_altitude')
        levels = range(0, 5001, minor)
        return (
            var.plot.contour(
                levels=[lev for lev in levels if lev % major == 0],
                ax=ax, colors=['0.25'], linewidths=0.25),
            var.plot.contour(
                levels=[lev for lev in levels if lev % major != 0],
                ax=ax, colors=['0.25'], linewidths=0.1))

    def surface_velocity(self, ax=None):
        """Plot surface velocity map."""
        var = self._ds.hyoga.getvar('magnitude_of_land_ice_surface_velocity')
        return var.plot.imshow(
            ax=ax, add_colorbar=False, alpha=0.75,
            cmap='Blues', norm=mcolors.LogNorm(1e1, 1e3))

    def surface_velocity_streamplot(self, ax=None, **kwargs):
        """Plot surface velocity streamlines."""
        uvar = self._ds.hyoga.getvar('land_ice_surface_x_velocity')
        vvar = self._ds.hyoga.getvar('land_ice_surface_y_velocity')
        ax = ax or plt.gca()

        # streamplot surface velocity
        try:
            return ax.streamplot(
                uvar.x, uvar.y, uvar.to_masked_array(), vvar.to_masked_array(),
                color=((uvar**2+vvar**2)**0.5).to_masked_array(),
                cmap='Blues', norm=mcolors.LogNorm(1e1, 1e3),
                arrowsize=0.25, linewidth=0.5, **kwargs)

        # streamplot colormapping fails on empty arrays (mpl issue #19323)
        except ValueError:
            return None
