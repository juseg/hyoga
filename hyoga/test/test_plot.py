# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

import numpy as np
import xarray as xr
import hyoga


def make_dataset():
    """Make minimal dataset with bedrock altitude and ice thickness."""
    darray = xr.DataArray(np.linspace(0, 1000, 6).reshape((2, 3)))
    ds = xr.Dataset({
        'b': darray.assign_attrs(standard_name='bedrock_altitude'),
        'h': darray.assign_attrs(standard_name='land_ice_thickness')})
    return ds


def test_ice_margin():
    ds = make_dataset()
    ds.hyoga.plot.ice_margin()
