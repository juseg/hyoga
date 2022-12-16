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


def test_bedrock_altitude():
    ds = make_dataset()
    ds.hyoga.plot.bedrock_altitude()


def test_bedrock_altitude_contours():
    ds = make_dataset()
    ds.hyoga.plot.bedrock_altitude_contours()


def test_bedrock_erosion():
    ds = make_dataset()
    ds = ds.assign(
        u=ds.b.assign_attrs(standard_name='land_ice_basal_x_velocity'),
        v=ds.b.assign_attrs(standard_name='land_ice_basal_y_velocity'))
    ds.hyoga.plot.bedrock_erosion()


def test_bedrock_hillshade():
    ds = make_dataset()
    ds.hyoga.plot.bedrock_hillshade()


def test_bedrock_isostasy():
    ds = make_dataset()
    ds = ds.assign(d=ds.b.assign_attrs(
        standard_name='bedrock_altitude_change_due_to_isostatic_adjustment'))
    ds.hyoga.plot.bedrock_isostasy()


def test_bedrock_shoreline():
    ds = make_dataset()
    ds.hyoga.plot.bedrock_shoreline()


def test_ice_margin():
    ds = make_dataset()
    ds.hyoga.plot.ice_margin()


def test_surface_altitude_contours():
    ds = make_dataset()
    ds.hyoga.plot.surface_altitude_contours()


def test_surface_hillshade():
    ds = make_dataset()
    ds.hyoga.plot.surface_hillshade()


def test_surface_velocity():
    ds = make_dataset()
    ds = ds.assign(
        u=ds.b.assign_attrs(standard_name='land_ice_surface_x_velocity'),
        v=ds.b.assign_attrs(standard_name='land_ice_surface_y_velocity'))
    ds.hyoga.plot.surface_velocity()


def test_surface_velocity_streamplot():
    ds = make_dataset()
    ds = ds.assign(
        u=ds.b.assign_attrs(standard_name='land_ice_surface_x_velocity'),
        v=ds.b.assign_attrs(standard_name='land_ice_surface_y_velocity'))
    ds.hyoga.plot.surface_velocity_streamplot()


def test_natural_earth():
    ds = make_dataset()
    ds.hyoga.plot.naturalearth()


def test_paleoglaciers():
    ds = make_dataset()
    ds.hyoga.plot.paleoglaciers()


def test_scale_bar():
    ds = make_dataset()
    ds.hyoga.plot.scale_bar()
