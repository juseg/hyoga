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
        # NOTE in the future we will decide here about age dim and units
        self._ds = dataset
        self._ds = self._fill_standard_names()
        self.plot = hyoga.plot.HyogaPlotMethods(dataset)

    def _fill_standard_names(self):
        """Add missing standard names in old PISM files.

        Currently this method only supports PISM. In the future other models
        will be supported, ideally detected using netCDF metadata, and
        otherwise through a keyword argument in hyoga.open methods."""
        pism_names = {
            'bedrock_altitude':                         'topg',
            'land_ice_basal_x_velocity':                'uvelbase',
            'land_ice_basal_y_velocity':                'vvelbase',
            'land_ice_surface_x_velocity':              'uvelsurf',
            'land_ice_surface_y_velocity':              'uvelsurf',
            'land_ice_thickness':                       'thk',
            'magnitude_of_land_ice_basal_velocity':     'velbase_mag',
            'magnitude_of_land_ice_surface_velocity':   'velsurf_mag',
            'surface_altitude':                         'usurf'}
        ds = self._ds
        for standard_name, name in pism_names.items():
            if name in self._ds and 'standard_name' not in ds[name].attrs:
                ds[name] = ds[name].assign_attrs(standard_name=standard_name)
        return ds

    def _safe_apply(self, func, *standard_names, **kwargs):
        """Apply a function to a list of variables after checking units."""

        # get vars and assert all units are the same (allowing None)
        variables = [self.getvar(name, **kwargs) for name in standard_names]
        units = variables[0].attrs.get('units')
        assert all(var.attrs.get('units') == units for var in variables)

        # compute new variable and assign common attributes
        # (np.all is necessary for arrays but also works on non-arrays)
        attrs = {
            k: v for k, v in variables[0].attrs.items() if
            all(np.all(var.attrs[k] == v) for var in variables)}
        return func(variables).assign_attrs(**attrs)

    def _safe_mag(self, *args, **kwargs):
        """Compute the magnitude of several variables if units match."""
        return self._safe_apply(
            lambda l: sum(v**2 for v in l)**0.5, *args, **kwargs)

    def _safe_sub(self, *args, **kwargs):
        """Compute the sum of several variables if units match."""
        assert len(args) == 2
        return self._safe_apply(lambda l: l[0]-l[1], *args, **kwargs)

    def _safe_sum(self, *args, **kwargs):
        """Compute the sum of two variables if units match."""
        return self._safe_apply(sum, *args, **kwargs)

    def assign_isostasy(self, datasource):
        """Compute bedrock isostatic adjustment using a separate file.

        Parameters
        ----------
        datasource: DataArray, str, Path, file-like or DataStore
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

        # read topography from file if it is not an array
        if not isinstance(datasource, xr.DataArray):
            with hyoga.open.dataset(datasource) as ds:
                topo = ds.hyoga.getvar('bedrock_altitude')

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
                return self._safe_sub(
                    'surface_altitude', 'land_ice_thickness', infer=False
                ).assign_attrs(standard_name=standard_name)
            if standard_name == 'land_ice_thickness':
                return self._safe_sub(
                    'surface_altitude', 'bedrock_altitude', infer=False
                ).assign_attrs(standard_name=standard_name)
            if standard_name == 'surface_altitude':
                return self._safe_sum(
                    'bedrock_altitude', 'land_ice_thickness', infer=False
                ).assign_attrs(standard_name=standard_name)

            # try to get the magnitude of a vector from its components
            if standard_name.startswith('magnitude_of_'):
                vector = standard_name.replace('magnitude_of_', '', 1)
                directions = directions or ('upward', 'downward', 'x', 'y')
                components = [
                    var.attrs['standard_name'] for var in self._ds.values() if
                    vector in [
                        var.attrs.get('standard_name', '').replace('_'+d, '')
                        for d in directions]]
                if len(components) > 0:
                    return self._safe_mag(*components).assign_attrs(
                        standard_name=standard_name)

        # really nothing worked, give up
        raise ValueError(
            "No variable found with standard name {}.".format(
                standard_name))

    def interp(self, datasource, ax=None, sigma=None, threshold=1):
        """Interpolate onto higher resolution topography for visualization.

        Parameters
        ----------
        datasource: DataArray, str, Path, file-like or DataStore
            Data array or path to file containing the high-resolution bedrock
            topography (standard name bedrock_altitude) or reference surface
            topography and ice thickness (standard names surface_altitude and
            land_ice_thickness) from which it is computed.
        ax : Axes, optional
            If axes are provided, "axes coordinates" will be generated so that
            the data are interpolated onto a grid where each point is a pixel
            in the current figure (using the current figure dpi). By default,
            the data are interpolated onto coordinates in the ``datasource``.
        sigma: float, optional
            Some batyhmetric datasets (e.g. ETOPO) are delivered with integer
            precision. This will cause artefacts in rendered paleo-shorelines
            on shallow slopes, looking especially strange if a float-precision
            isostatic correction is applied on the integer-precision elevation
            data. This parameter activates a mechanism that attempts to smooth
            shallow slopes with little effect on steep mountains. The value
            for ``sigma`` is the gaussian window size in projections units.
        threshold: float, optional
            Thickness threshold used to compute a glacier mask. The mask will
            be refined after interpolation, so that any mountains in the
            high-resolution topography that are higher than the interpolated
            ice surface will appear as nunataks in the visualization.

        Returns
        -------
        dataset : Dataset
            The interpolated dataset, with new horizontal resolution
            corresponding to either the data provided in ``datasource``, or
            the pixel count of axes provided with ``ax``.
        """

        # read topography from file if it is not an array
        if not isinstance(datasource, xr.DataArray):
            with hyoga.open.dataset(datasource) as ds:
                topo = ds.hyoga.getvar('bedrock_altitude')

        # get interpolation coordinates
        if ax is not None:
            x, y = _coords_from_axes(ax)
            topo = topo.interp(x=x, y=y)
        else:
            x = topo.x
            y = topo.y

        # try to smooth integer-precision steps
        if sigma is not None:
            dx = (x[-1]-x[0])/(len(x)-1)
            dy = (y[-1]-y[0])/(len(y)-1)
            assert abs(dy-dx) < 1e12
            topo = topo.astype(float)  # convert to float
            filt = scipy.ndimage.gaussian_filter(topo, sigma=sigma/dx)
            topo += np.clip(filt-topo, -0.5, 0.5)

        # lookup bedrock_topography short name, default to topg
        try:
            name = ds.hyoga.getvar('bedrock_topography').name
        except ValueError:
            name = None
        name = name or topo.name or 'topg'

        # interpolate data variables and assign new topo
        ds = self._ds.interp(x=x, y=y).assign({name: topo})

        # correct for isostasy if it is present
        try:
            ds[name] += ds.hyoga.getvar(
                'bedrock_altitude_change_due_to_isostatic_adjustment')
        except ValueError:
            pass

        # interp mask and refine based on interpolated surface
        # NOTE will throw an error if thk or usurf is missing
        icy = self.getvar('land_ice_thickness') > threshold
        icy = (1*icy).interp(x=x, y=y)
        icy = (icy >= 0.5) * (ds.hyoga.getvar('surface_altitude') > ds[name])
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
