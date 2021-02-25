# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module extends xarray datasets with methods specific to ice-sheet model
output, such as finding variables by standard name, computing bedrock uplift,
masking and interpolation. This functionality is made available through an
xarray dataset 'ice' accessor. Plotting methods are kept in a separate module.
"""

import warnings
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

    def assign_isostasy(self, datasource):
        """Compute bedrock isostatic adjustment using a separate file.

        Parameters
        ----------
        datasource: DataArray, srt, Path, file-like or DataStore
            Data array or path to file containing the reference bedrock
            topography (standard name bedrock_altitude) or reference surface
            topography and ice thickness (standard names surface_altitude and
            land_ice_thickness) from which it is computed.

        Returns
        -------
        dataset : Dataset
            The dataset with added uplift variable, with variable name
            "isostasy" (warn and add trailing underscores if taken) and
            standard name "bedrock_altitude_change_due_to_isostatic_adjustment"
            (warn and create a duplicate if standard name is taken).
        """

        # warn if bedrock isostatic appears to be present in dataset
        # NOTE: in the future we may consider an override switch, and perhaps a
        # separate method to assign variables by standard name
        ds = self._ds
        standard_name = 'bedrock_altitude_change_due_to_isostatic_adjustment'
        for name, var in ds.items():
            if var.attrs.get('standard_name', '') == standard_name:
                warnings.warn(
                    "found existing variable {} with standard name {} while"
                    "computing bedrock isostatic adjustment, will result in"
                    "a duplicate".format(name, standard_name), UserWarning)

        # add trailing underscores until we find a free variable name
        variable_name = 'isostasy'
        while variable_name in ds:
            warnings.warn(
                "found existing variable {name} while computing bedrock"
                "isostatic adjustment, using {name}_ instead".format(
                    name=variable_name), UserWarning)
            variable_name += '_'

        # read topography from file if it is not an array
        if not isinstance(datasource, xr.DataArray):
            with hyoga.open.dataset(datasource) as ds:
                topo = ds.hyoga.getvar('bedrock_altitude')

        # compute bedrock isostatic adjustment
        ds[variable_name] = (
            ds.hyoga.getvar('bedrock_altitude')-topo).assign_attrs(
                standard_name=standard_name)
        return ds

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
        array : DataArray
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
                vector = standard_name.replace('magnitude_of_', '', 1)
                directions = directions or ('upward', 'downward', 'x', 'y')
                components = [
                    var for var in self._ds.values() if vector in [
                        var.attrs.get('standard_name', '').replace('_'+d, '')
                        for d in directions]]
                if len(components) > 0:
                    return sum(var**2 for var in components)**0.5

        # really nothing worked, give up
        raise ValueError(
            "No variable found with standard name {}.".format(
                standard_name))

    def interp(self, filename, ax=None, sigma=None):
        """Interpolate onto higher resolution topography for visualization."""
        # FIXME replace filename by datasource

        # load hires bedrock topography
        with hyoga.open.dataset(filename) as ds:
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

        # assign ice mask and interpolate all variables
        # FIXME use standard names, what if thk is missing?
        ds = self._ds.assign(icy=ds.thk.fillna(0) > 0)
        ds = ds.interp(x=x, y=y)

        # interpolate hires topography
        # FIXME has no effect if ax is None
        ds['topg'] = hires.interp(x=x, y=y)

        # correct for uplift if present
        # FIXME use standard names
        if 'uplift' in ds:
            ds['topg'] = ds.topg + ds.uplift.fillna(0.0)

        # refine ice mask based on interpolated values
        # FIXME use standard names, what if usurf or topg is missing?
        icy = (ds.icy >= 0.5) * (ds.usurf > ds.topg)

        # apply interpolated mask on glacier variables
        ds = ds.hyoga.where(icy)

        # return interpolated data
        return ds

    def where(self, cond, **kwargs):
        """Filter glacier (non-bedrock) variables according to a condition.

        Parameters
        ----------
        cond : DataArray, Dataset, or callable
            Locations at which to preserve glacier variables.
        **kwargs : optional
            Additional keyword arguments are passed to
            :meth:`xarray.Dataset.where`.

        Returns
        -------
        dataset : Dataset
            Corresponing dataset with variables whose standard name does not
            start with "bedrock_altitude" filtered by the condition.
        """
        ds = self._ds
        for name, var in ds.items():
            if not var.attrs.get(
                    'standard_name', '').startswith('bedrock_altitude'):
                ds[name] = var.where(cond, **kwargs)
        return ds

    def where_thicker(self, threshold=1, **kwargs):
        """Filter glacier (non-bedrock) variables using a thickness threshold.

        Parameters
        ----------
        threshold : scalar
            Thickness below which to mask glacier variables.
        **kwargs : optional
            Additional keyword arguments are passed to
            :meth:`xarray.Dataset.where`.

        Returns
        -------
        dataset : Dataset
            Corresponing dataset with variables whose standard name does not
            start with "bedrock_altitude" masked below threshold.
        """
        return self.where(
            self.getvar('land_ice_thickness') >= threshold, **kwargs)
