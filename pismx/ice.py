# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module extends xarray datasets with methods specific to ice-sheet model
output, such as finding variables by standard name, computing bedrock uplift,
masking and interpolation. This functionality is made available through an
xarray dataset 'ice' accessor. Plotting methods are kept in a separate module.
"""

import numpy as np
import scipy.ndimage
import xarray as xr
import pismx.open
import pismx.plot


def _coords_from_axes(ax):
    """Compute coordinate vectors from matplotlib axes."""
    bbox = ax.get_window_extent()
    return _coords_from_extent(
        ax.get_extent(), int(round(bbox.width)), int(round(bbox.height)))


def _coords_from_extent(extent, cols, rows):
    """Compute coordinate vectors from image extent."""

    # compute dx and dy
    (west, east, south, north) = extent
    dx = (east-west) / cols
    dy = (north-south) / rows

    # prepare coordinate vectors
    xwcol = west + 0.5*dx  # x-coord of W row cell centers
    ysrow = south + 0.5*dy  # y-coord of N row cell centers
    x = xwcol + np.arange(cols)*dx  # from W to E
    y = ysrow + np.arange(rows)*dy  # from S to N

    # return coordinate vectors
    return x, y


@xr.register_dataset_accessor('ice')
class IceDataset:
    """PISMX extension to xarray datasets."""

    def __init__(self, dataset):
        self._ds = dataset
        self.plot = pismx.plot.IcePlotMethods(dataset)

    def interp(self, bootfile, interpfile, ax=None, sigma=None,
               variables=None, **kwargs):
        """Interpolate onto higher resolution topography for visualization."""
        # FIXME: include all vars by defaults, cause little slowdown

        # load hires bedrock topography
        with pismx.open.dataset(interpfile) as ds:
            hires = ds.usurf.fillna(0.0) - ds.thk.fillna(0.0)

        # interpolation coordinates
        if ax is not None:
            x, y = _coords_from_axes(ax)
        else:
            x = hires.x
            y = hires.y

        # try to smooth integer-precision steps
        # NOTE: is it possible to avoid scipy.ndimage?
        if sigma is not None:
            dx = (x[-1]-x[0])/(len(x)-1)
            dy = (y[-1]-y[0])/(len(y)-1)
            assert abs(dy-dx) < 1e12
            filt = scipy.ndimage.gaussian_filter(hires, sigma=float(sigma/dx))
            hires += np.clip(filt-hires, -1.0, 1.0)

        # load boot topo
        # NOTE: make boot topo optional?
        with pismx.open.dataset(bootfile) as ds:
            boot = ds.topg

        # compute ice mask and bedrock uplift
        # FIXME compute ice mask elsewhere
        ds = self._ds
        ds['icy'] = 1.0 * (ds.thk >= 1.0)
        ds['uplift'] = ds.topg - boot

        # interpolate surfaces to axes coords
        ds = ds[['icy', 'uplift', 'usurf']+(variables or [])]
        ds = ds.interp(x=x, y=y)

        # interpolate hires topography
        ds['topg'] = hires.interp(x=x, y=y)

        # correct basal topo for uplift
        ds['topg'] = ds.topg + ds.uplift.fillna(0.0)

        # refine ice mask based on interpolated values
        ds['icy'] = (ds.icy >= 0.5) * (ds.usurf > ds.topg)

        # apply interpolated mask on glacier variables
        for var in ['usurf']+(variables or []):
            ds[var] = ds[var].where(ds.icy)

        # return interpolated data
        return ds
