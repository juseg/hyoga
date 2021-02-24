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
import hyoga.open
import hyoga.plot


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


@xr.register_dataset_accessor('hyoga')
class HyogaDataset:
    """Hyoga extension to xarray datasets."""

    def __init__(self, dataset):
        self._ds = dataset
        self.plot = hyoga.plot.HyogaPlotMethods(dataset)

    def getvar(self, standard_name, infer=True, directions=None):
        """Get a variable by conventional standard name.

        Parameters
        ----------
        standard_name : str
            The variable's "standard_name" attribute, which in principle
            should be set according to netCDF Climate and Forecast (CF)
            conventions (http://cfconventions.org/standard-names.html).
        infer : bool
            Try to infer missing variables from others present in the dataset.
            If one of the topographic variables ("bedrock_altitude",
            "land_ice_thickness", and "surface_altitude") is requested and
            missing from the data, try to compute it from the other two.
            If a variable name starting with "magnitude_of" is requested and
            missing, try to compute it as the norm of its components.
        directions : iterable
            Allowed direction keywords for computing vector magnitudes.
            Defaults to ("upward", "downward", "x", "y"). Computing magnitudes
            on a sphere is not supported and thus longitude and latitude
            directions ("northward", "southward", "eastward", "westward")
            are not included by default.

        Returns
        -------
        array : :class:`xarray.DataArray`
            The data array corresponding to that variable if a unique variable
            with that standard name has been found.

        Raises
        ------
        ValueError
            If either more or less than one variable with the corresponding
            standard name are found.
        """

        # filter dataset by standard name
        matching = self._ds.filter_by_attrs(standard_name=standard_name)

        # one variable found, return it
        if len(matching) == 1:
            return matching[list(matching.data_vars)[0]]

        # more than one variable, raise an error
        if len(matching) > 1:
            raise ValueError(
                "Several variables ({}) match standard name {}".format(
                    matching.data_vars, standard_name))

        # no variable found, try to compute it from other variables
        # (infer=False is needed to avoid infinite recursion)
        if infer is True:
            if standard_name == 'bedrock_altitude':
                return (
                    self.getvar('surface_altitude', infer=False) -
                    self.getvar('land_ice_thickness', infer=False))
            if standard_name == 'land_ice_thickness':
                return (
                    self.getvar('surface_altitude', infer=False) -
                    self.getvar('bedrock_altitude', infer=False))
            if standard_name == 'surface_altitude':
                return (
                    self.getvar('bedrock_altitude', infer=False) +
                    self.getvar('land_ice_thickness', infer=False))

            # try to get the magnitude of a vector from its components
            if standard_name.startswith('magnitude_of_'):
                vector = standard_name.removeprefix('magnitude_of_')
                directions = directions or ('upward', 'downward', 'x', 'y')
                components = [
                    var for name, var in self._ds.items() if 'standard_name' in
                    var.attrs and vector in [
                        var.attrs['standard_name'].replace('_'+d, '') for d in
                        directions]]
                if len(components) > 0:
                    return sum(var**2 for var in components)**0.5

        # really nothing worked, give up
        raise ValueError(
            "No variable found with standard name {}.".format(
                standard_name))

    def interp(self, bootfile, interpfile, ax=None, sigma=None,
               variables=None, **kwargs):
        """Interpolate onto higher resolution topography for visualization."""
        # FIXME: include all vars by defaults, cause little slowdown

        # load hires bedrock topography
        with hyoga.open.dataset(interpfile) as ds:
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
        with hyoga.open.dataset(bootfile) as ds:
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
