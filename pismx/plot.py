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
import cartowik.conventions as ccv
import cartowik.shadedrelief as csr


class IcePlotMethods:
    """
    A namespace to keep all plot methods in one place.
    """

    def __init__(self, dataset):
        self._ds = dataset

    def bedrock_erosion(self, ax=None):
        """Plot erosion rate based on basal velocity."""
        ds = self._ds
        return (5.2e-8*ds.velbase_mag**2.34).plot.contourf(
                ax=ax, add_colorbar=False, alpha=0.75, cmap='YlOrBr',
                levels=[10**i for i in range(-9, 1)])

    def bedrock_shaded_relief(self, ax=None, sealevel=0, style='grey'):
        """Plot bedrock topography shaded relief and shoreline."""
        ds = self._ds

        # plot topography and sea level contour
        (ds.topg-sealevel).plot.imshow(
            ax=ax, add_colorbar=False, zorder=-1,
            cmap=(ccv.ELEVATIONAL if style == 'wiki' else 'Greys'),
            vmin=(-4500 if style == 'wiki' else 0), vmax=4500)
        csr.add_multishade(
            ds.topg, ax=ax, add_colorbar=False, zorder=-1)
        (ds.topg-sealevel).plot.contour(
            ax=ax, colors=('#0978ab' if style == 'wiki' else '0.25'),
            levels=[0], linestyles='dashed', linewidths=0.25, zorder=0)

    def bedrock_uplift(self, ax=None):
        """Plot bedrock deformation contours."""
        ds = self._ds

        # locate maximum depression (xarray has no idxmin yet)
        ax = ax or plt.gca()
        i, j = divmod(int(ds.uplift.argmin()), ds.uplift.shape[1])
        maxdep = float(-ds.uplift[i, j])
        color = 'w' if maxdep > 50 else 'k'
        ax.plot(ds.x[j], ds.y[i], 'o', color=color, alpha=0.75)
        ax.annotate(
            '{:.0f} m'.format(maxdep), color=color, xy=(ds.x[j], ds.y[i]),
            xytext=(3, 3), textcoords='offset points')

        # plot bedrock deformation contours
        return ds.uplift.plot.contourf(
            ax=ax, add_colorbar=False, alpha=0.75, cmap='PRGn_r',
            levels=[-100, -50, -20, 0, 2, 5, 10])

    def ice_margin(self, ax=None, edgecolor='0.25', facecolor=None, **kwargs):
        """Plot ice margin line and/or filled contour."""
        ds = self._ds
        # FIXME make variable customizable
        contours = []
        if edgecolor is not None:
            contours.append(ds.thk.notnull().plot.contour(
                ax=ax, colors=edgecolor, levels=[0.5], linewidths=0.25,
                **kwargs))
        if facecolor is not None:
            contours.append(ds.thk.notnull().plot.contourf(
                ax=ax, add_colorbar=False, colors=facecolor, extend='neither',
                levels=[0.5, 1.5], **kwargs))
        return contours if len(contours) > 1 else contours[0]

    def surface_velocity(self, ax=None):
        """Plot surface velocity map."""
        ds = self._ds
        if 'velsurf_mag' not in ds:
            ds['velsurf_mag'] = (ds.uvelsurf**2+ds.vvelsurf**2)**0.5
        return ds.velsurf_mag.plot.imshow(
            ax=ax, add_colorbar=False, alpha=0.75,
            cmap='Blues', norm=mcolors.LogNorm(1e1, 1e3))

    def surface_velocity_streamplot(self, ax=None, **kwargs):
        """Plot surface velocity streamlines."""

        ds = self._ds
        ax = ax or plt.gca()

        # streamplot surface velocity
        try:
            return ax.streamplot(
                ds.x, ds.y,
                ds.uvelsurf.to_masked_array(),
                ds.vvelsurf.to_masked_array(),
                color=((ds.uvelsurf**2+ds.vvelsurf**2)**0.5
                       ).to_masked_array(),
                cmap='Blues', norm=mcolors.LogNorm(1e1, 1e3),
                arrowsize=0.25, linewidth=0.5, **kwargs)

        # streamplot colormapping fails on empty arrays (mpl issue #19323)
        except ValueError:
            return None

    def surface_topo_contours(self, ax=None, minor=200, major=1000):
        """Plot minor and major surface topography contours."""
        ds = self._ds
        levels = range(0, 5001, minor)
        return (
            ds.usurf.plot.contour(
                levels=[lev for lev in levels if lev % major == 0],
                ax=ax, colors=['0.25'], linewidths=0.25),
            ds.usurf.plot.contour(
                levels=[lev for lev in levels if lev % major != 0],
                ax=ax, colors=['0.25'], linewidths=0.1))
