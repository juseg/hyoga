#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Plot Akaishi paleoglaciers map."""

import os.path
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.img_tiles
import cartowik.naturalearth as cne
import cartowik.shadedrelief as csr


# FIXME all duplicates of logo code
def add_countries(ax, scale=None, **kwargs):
    """Add Natural Earth Data countries."""
    return ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            category='cultural', name='admin_0_countries', scale=scale),
        **kwargs)


def add_glaciers(ax, scale=None, **kwargs):
    """Add Natural Earth Data glaciers."""
    return ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            category='physical', name='glaciated_areas', scale=scale),
        **kwargs)


def add_broken_shapefile(ax, filename, **kwargs):
    """Ehlers et al. (2011) data has duplicates."""
    ax = ax or plt.gca()
    crs = cartopy.crs.PlateCarree()
    shp = cartopy.io.shapereader.Reader(filename)
    geometries = []
    for geom in shp.geometries():
        if geom not in geometries:
            geometries.append(geom)
    return ax.add_geometries(geometries, crs, **kwargs)


# FIXME move this into new submodule, e.g. cartowik.webdatasets.srtm()?
def getsrtm(output='srtm.tif', product='SRTM1', **kwargs):
    """Retrieve SRTM data, return cached filename."""
    import os.path
    import elevation
    elevation.clip(output=output, product=product, **kwargs)
    return os.path.join(elevation.CACHE_DIR, product, output)


def make_akaishi_stamen_terrain():
    """Draw map with stamen terrain background."""

    # init stamen layer
    stamen = cartopy.io.img_tiles.Stamen('terrain-background')

    # axes with stamen projection
    ax = plt.axes([0, 0, 1, 1], projection=stamen.crs)
    ax.set_extent([15330e3, 15450e3, 4200e3, 4290e3], crs=ax.projection)

#    # axes with laea projection
#    ax = plt.axes(
#        [0, 0, 1, 1], projection=cartopy.crs.LambertAzimuthalEqualArea(
#            central_longitude=138, central_latitude=36))
#    ax.set_extent([-40e3, 80e3, -90e3, 0e3], crs=ax.projection)

    # add stamen terrain
    ax.add_image(stamen, 11)

    # add glaciers (cne more efficient due to cropping)
    cne.add_shapefile(
        os.path.expanduser('~/.cache/hyoga/lgm.shp'),
        ax=ax, alpha=0.75, facecolor='w', edgecolor='w')

    # return figure to save
    return ax.figure


def make_akaishi_srtm_elevation():
    """Draw map with srtm elevation background."""

    # background srtm elevation
    import rioxarray  # noqa
    import rasterio.enums
    ax = plt.axes(
        [0, 0, 1, 1], projection=cartopy.crs.LambertAzimuthalEqualArea(
            central_longitude=138, central_latitude=36))
    ax.set_extent([-40e3, 80e3, -90e3, 0e3], crs=ax.projection)
    srtm = getsrtm(bounds=(137, 35, 139, 36))
    srtm = csr._open_data_source(srtm)
    srtm = srtm.rio.write_crs('+proj=lonlat')
    srtm = srtm.rio.reproject(
        ax.projection.proj4_init,
        resampling=rasterio.enums.Resampling.bilinear, resolution=90e3/1080/2)
    csr.add_topography(srtm, cmap='Greys', vmin=0, vmax=4500)
    csr.add_multishade(srtm, azimuths=[255, 315, 315, 15])

    # add physical elements
    cne.add_rivers(ax=ax, edgecolor='0.25')
    cne.add_lakes(ax=ax, edgecolor='0.25', facecolor='0.75')
    cne.add_coastline(ax=ax, edgecolor='0.25')
    cne.add_graticules(ax=ax, interval=5)

    # add glaciers (cne more efficient due to cropping)
    color = 'tab:red'  # plt.get_cmap('Blues')(256)
    cne.add_shapefile(
        os.path.expanduser('~/.cache/hyoga/lgm.shp'),
        alpha=0.75, ax=ax, facecolor=color, edgecolor=None)

    # return figure to save
    return ax.figure


def main():
    """Main program called during execution."""
#    fig = make_akaishi_stamen_terrain()
#    fig.savefig(__file__[:-3]+'_stamen_terrain', dpi=300)
    fig = make_akaishi_srtm_elevation()
    fig.savefig(__file__[:-3]+'_srtm_elevation', dpi=300)


if __name__ == '__main__':
    main()
