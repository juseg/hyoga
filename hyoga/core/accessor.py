# Copyright (c) 2021-2024, Julien Seguinot (juseg.dev)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module extends xarray datasets with methods specific to ice-sheet model
output, such as finding variables by standard name, computing bedrock uplift,
masking and interpolation. This functionality is made available through an
xarray dataset accessor. Plotting methods are kept in a separate module.
"""

import warnings
import geopandas
import numpy as np
import scipy.ndimage
import xarray as xr
import cf_xarray  # noqa pylint: disable=unused-import

import hyoga.plot.datasets


def _coords_from_axes(ax):
    """Compute coordinate vectors from matplotlib axes."""
    bbox = ax.get_window_extent()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    return _coords_from_extent(
        (*xlim, *ylim), int(round(bbox.width)), int(round(bbox.height)))


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


def _open_datasource(datasource, standard_name):
    """Get variable from dataset or file, or return data array."""
    if isinstance(datasource, xr.DataArray):
        return datasource
    if isinstance(datasource, xr.Dataset):
        return datasource.hyoga.getvar(standard_name)
    with xr.open_dataset(datasource) as ds:
        return ds.hyoga.getvar(standard_name)


@xr.register_dataset_accessor('hyoga')
class HyogaDataset:
    """Hyoga extension to xarray datasets."""

    # needed for sphinx etc to see plot methods
    plot = xr.core.utils.UncachedAccessor(hyoga.plot.datasets.HyogaPlotMethods)

    def __init__(self, dataset):
        """Initialize data accessor.

        The accessed data set is decoded according to CF conventions, then
        heuristics are used to try and fill missing standard names. This latter
        step is necessary to inform secondary coordinates referred in the
        'coordinates' attribute, otherwise `dataset.cf[standard_name]` may have
        different coordinates than `dataset`, causing a MergeError in variable
        assignment and masking operations.

        Parameters
        ----------
        dataset : Dataset on which the accessor is plugged.
        """
        # NOTE in the future we will decide here about age dim and units
        self._ds = xr.decode_cf(dataset)
        self._ds = self._fill_standard_names()

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

    def assign(self, **standard_variables):
        """Assign new variables by standard_name.

        Parameters
        ----------
        standard_variables : mapping
            A mapping from netCDF Climate and Forecast compliant standard names
            (http://cfconventions.org/standard-names.html), to data arrays, or
            datasets or paths to files containing variables with the
            corresponding standard name.

        Returns
        -------
        dataset : Dataset
            A new dataset with the new variables added, replacing any existing
            variable with the same standard name. New variables are labelled
            according to their input (short) names, or standard names if short
            names are missing, with added trailing underscores in the event of
            duplicates.
        """

        # create an empty dict to store variables by short name
        variables = {}

        # read data from source if it is not already an array
        for standard_name, datasource in standard_variables.items():
            data = _open_datasource(datasource, standard_name)
            data = data.assign_attrs(standard_name=standard_name)

            # default to existing name, else standard name
            variable_name = data.name or standard_name

            # look for existing variable with given standard name
            variable_found = False
            for name, var in self._ds.items():
                if var.attrs.get('standard_name', '') == standard_name:
                    variable_name = name
                    variable_found = True
                    break

            # if variable_name is present, but matches a different standard
            # name, add trailing underscores until we find a free slot
            while variable_found is False and variable_name in self._ds:
                warnings.warn(
                    f"found existing variable {variable_name}, using "
                    f"{variable_name}_ instead", UserWarning)
                variable_name += '_'

            # link variable data to short name (skip coords, see #74)
            variables[variable_name] = data.variable

        # assign new variables and return a new dataset
        return self._ds.assign(variables)

    def assign_icemask(self, datasource, name='icemask'):
        """Assign an ice mask corresponding to glacierized area.

        Hyoga looks for this variable in most plot methods, and defaults to
        considering any grid cell with non-zero ice thickness as glacierized.

        Parameters
        ----------
        datasource : DataArray, Dataset, str, Path, file-like or DataStore
            Data array, or a dataset or path to a file containing the ice mask
            (standard name "land_ice_area_fraction").
        name : string, optional
            Default name for the new ice mask variable. Not used if standard
            name "land_ice_area_fraction" is already present in the dataset.

        Returns
        -------
        dataset : Dataset
            The dataset with added ice mask variable, with standard name
            "land_ice_area_fraction" (replacing existing variables).
        """
        return self.assign(land_ice_area_fraction=datasource.rename(name))

    def assign_isostasy(self, datasource, name='isostasy'):
        """Compute bedrock isostatic adjustment using a separate file.

        Parameters
        ----------
        datasource : DataArray, Dataset, str, Path, file-like or DataStore
            Data array, or a dataset or path to a file containing the reference
            bedrock topography (standard name "bedrock_altitude") or the
            reference surface topography and ice thickness (standard names
            "surface_altitude" and "land_ice_thickness") from which it is
            computed.
        name : string, optional
            Default name for the new isostasy variable. Not used if standard
            name "bedrock_altitude_change_due_to_isostatic_adjustment" is
            already present in the dataset.

        Returns
        -------
        dataset : Dataset
            The dataset with added uplift variable, with standard name
            "bedrock_altitude_change_due_to_isostatic_adjustment" (replacing
            existing variables).
        """

        # read topo if not an array and compute bedrock isostatic adjustment
        topo = _open_datasource(datasource, 'bedrock_altitude')
        diff = self.getvar('bedrock_altitude') - topo

        # assign new variable
        return self.assign(
            bedrock_altitude_change_due_to_isostatic_adjustment=diff.rename(
                name))

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
        """

        # if variable is present, return it
        if standard_name in self._ds.cf:
            return self._ds.cf[standard_name]

        # no variable found, try to compute it from other variables
        if infer is True:

            # try to get ice mask from ice thickness
            if standard_name == 'land_ice_area_fraction':
                return (
                    self.getvar('land_ice_thickness') >=
                    hyoga.config.glacier_masking_point
                ).astype(float).assign_attrs(standard_name=standard_name)

            # try to compute altitude and thickness variables
            # (infer=False is needed to avoid infinite recursion)
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
            f"No variable found with standard name {standard_name}.")

    def interp(self, datasource, ax=None, sigma=None):
        """Interpolate onto higher resolution topography for visualization.

        Parameters
        ----------
        datasource: DataArray, Dataset, str, Path, file-like or DataStore
            Data array, or a dataset or path to a file containing the reference
            bedrock topography (standard name bedrock_altitude) or the
            reference surface topography and ice thickness (standard names
            surface_altitude and land_ice_thickness) from which it is computed.
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

        Returns
        -------
        dataset : Dataset
            The interpolated dataset, with new horizontal resolution
            corresponding to either the data provided in ``datasource``, or
            the pixel count of axes provided with ``ax``. The ice surface
            altitude will be assigned if missing, to compute a detailed mask.
        """

        # read topography from file if it is not an array
        topo = _open_datasource(datasource, 'bedrock_altitude')

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

        # make sure surface altitude is present, needed for a nice mask
        # NOTE: add a wrapper something like ensure_var, maybe setvar?
        ds = self.assign(
            surface_altitude=self.getvar('surface_altitude').rename('usurf'))

        # make sure ice mask is present and has numeric type
        icemask = ds.hyoga.getvar('land_ice_area_fraction')
        ds = ds.hyoga.assign_icemask(icemask.astype(float))

        # interpolate data variables and assign new topo
        ds = ds.interp(x=x, y=y)

        # correct for isostasy if it is present
        try:
            topo += ds.hyoga.getvar(
                'bedrock_altitude_change_due_to_isostatic_adjustment')
        except ValueError:
            pass

        # assign corrected bedrock topography
        ds = ds.hyoga.assign(bedrock_altitude=topo.rename('topg'))

        # refine ice mask based on interpolated surface
        icemask = ds.hyoga.getvar('land_ice_area_fraction')
        icemask *= ds.hyoga.getvar('surface_altitude') > topo
        ds = ds.hyoga.assign_icemask(icemask)

        # return interpolated data
        return ds

    def profile(self, datasource, interval=None):
        """Interpolate onto coordinates along a profile.

        Parameters
        ----------
        datasource : sequence, array, GeoDataFrame, str, Path or file-like
            Sequence of (x, y) coordinate tuples, (N, 2) coordinate array,
            GeoDataFrame or path to a shapefile containing a single line,
            along which the dataset will be interpolated.
        interval : float, optional
            If provided, resample (linearly interpolate) profile coordinates
            to a fixed spatial resolution given by ``interval``. If ``None``,
            the data are interpolated to the exact ``datasource`` coordinate,
            which may produce an irreguar grid.

        Returns
        -------
        dataset : Dataset
            The interpolated dataset, where horizontal dimensions ``x`` and
            ``y`` are replaced by a new dimension ``d`` with a grid spacing of
            either ``interval`` or the distance between points in
            ``datasource``.
        """

        # read profile from datasource
        if isinstance(datasource, list):
            x, y = np.array(datasource).T
        elif isinstance(datasource, np.ndarray):
            x, y = datasource.T
        elif isinstance(datasource, geopandas.GeoDataFrame):
            x, y = datasource.squeeze().geometry.coords.xy
        else:
            datasource = geopandas.read_file(datasource)
            x, y = datasource.squeeze().geometry.coords.xy

        # compute distance along profile
        dist = ((np.diff(x)**2+np.diff(y)**2)**0.5).cumsum()
        dist = np.insert(dist, 0, 0)

        # build coordinate xarrays
        x = xr.DataArray(x, coords=[dist], dims='d')
        y = xr.DataArray(y, coords=[dist], dims='d')

        # if interval was given, interpolate coordinates
        if interval is not None:
            dist = np.arange(0, dist[-1], interval)
            x = x.interp(d=dist, method='linear')
            y = y.interp(d=dist, method='linear')

        # temporary workaround for scipy 1.10.0 issue 17718
        ds = self._ds
        if scipy.__version__ == "1.10.0":
            x_dtype = x.dtype
            y_dtype = y.dtype
            x = x.astype('float64')
            y = y.astype('float64')
            ds = ds.astype('float64')

        # interpolate dataset to new coordinates
        ds = ds.interp(x=x, y=y, method='linear', assume_sorted=True)

        # return to original precision (scipy 1.10.0 issue 17718)
        if scipy.__version__ == "1.10.0":
            x = x.astype(x_dtype)
            y = y.astype(y_dtype)
            for var in ds:
                ds[var] = ds[var].astype(self._ds[var].dtype)

        # set new coordinate attributes
        ds.d.attrs.update(long_name='distance along profile')
        if 'units' in self._ds.x.attrs:
            ds.d.attrs.update(units=self._ds.x.units)

        # return interpolated dataset
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
        ds = self._ds.copy()
        for name, var in ds.items():
            if not var.attrs.get(
                    'standard_name', '').startswith('bedrock_altitude'):
                ds[name] = var.where(cond, **kwargs)
        return ds

    def where_icemask(self, threshold=0.5, **kwargs):
        """Filter glacier (non-bedrock) variables using existing ice mask.


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
            start with "bedrock_altitude" masked by ice mask.
        """
        return self.where(
            self.getvar('land_ice_area_fraction') >= threshold, **kwargs)

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
