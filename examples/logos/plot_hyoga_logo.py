#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Plot logo for hyoga."""


import os.path
import zipfile
import matplotlib.pyplot as plt
import cartopy
import hyoga.demo
import hyoga.plot


def add_paleoglaciers(ax, **kwargs):
    """Add Ehlers et al. (2011) paleoglaciers."""
    paths = download_paleoglaciers()
    return tuple(add_broken_shapefile(ax, path, **kwargs) for path in paths)


def add_paleoglaciers_bat19(ax, **kwargs):
    """Add Batchelor et al. (2019) paleoglaciers."""
    paths = download_paleoglaciers_bat19()
    return tuple(add_broken_shapefile(ax, path, **kwargs) for path in paths)


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


def download_paleoglaciers():
    """Download Ehlers et al. (2011) paleoglaciers in cache dir."""
    url = ('http://static.us.elsevierhealth.com/ehlers_digital_maps/'
           'digital_maps_02_all_other_files.zip')
    zipfilename = hyoga.demo._download(url)
    cachedir = os.path.dirname(zipfilename)
    basenames = 'lgm', 'lgm_alpen'
    for basename in basenames:
        for ext in ('dbf', 'shp', 'shx'):
            filename = basename + '.' + ext
            if not os.path.isfile(os.path.join(cachedir, filename)):
                with zipfile.ZipFile(zipfilename, 'r') as archive:
                    archive.extract(filename, path=cachedir)
    return (os.path.join(cachedir, b+'.shp') for b in basenames)


def download_paleoglaciers_bat19():
    """Download Batchelor et al. (2019) paleoglaciers in cache dir."""
    files = {'https://osf.io/gzkwc/download': 'LGM_best_estimate.dbf',
             'https://osf.io/xm6tu/download': 'LGM_best_estimate.prj',
             'https://osf.io/9bjwn/download': 'LGM_best_estimate.shx',
             'https://osf.io/9yhdv/download': 'LGM_best_estimate.shp'}
    for url, filename in files.items():
        filepath = hyoga.demo._download(url, filename=filename)
    return (filepath, )


def draw_map(fig, rect):
    """Draw logo glaciers map."""

    # add map axes
    ax = fig.add_axes(rect, projection=cartopy.crs.Orthographic(
        central_longitude=-45, central_latitude=90))
    ax.patch.set_facecolor('tab:blue')
    ax.spines['geo'].set_edgecolor('none')

    # ax.set_extent does not work well with ortho proj
    ax.set_xlim((-6.4e6, 6.4e6))
    ax.set_ylim((-6.4e6, 6.4e6))

    # add continents and glaciers
    # tried so far
    # - red and white
    # - blue and white
    # - grey and cmap 256 blue
    # - grey and cmap 192 blue
    # - grey and tab:blue
    # color = 'k'  # 'tab:blue'  #plt.get_cmap('Blues')(192)
    hyoga.plot.countries(ax=ax, alpha=0.25, facecolor='w', scale='110m')
    add_paleoglaciers_bat19(ax=ax, alpha=0.75, facecolor='w', zorder=1)
    hyoga.plot.glaciers(ax=ax, edgecolor='w', facecolor='w', scale='50m',
                        zorder=2)


def draw_text(fig, rect):
    """Draw logo japanese text."""
    plt.rc('font', family='TakaoPGothic')
    ax = fig.add_axes(rect)
    bbox = ax.get_window_extent()
    height = bbox.height/fig.dpi*72
    kwargs = dict(fontsize=0.4*height, va='center')
    ax.text(0.2, 0.7, '氷', **kwargs)
    ax.text(0.2, 0.2, '河', **kwargs)
    kwargs = dict(fontsize=0.05*height, linespacing=1.5, va='center')
    ax.text(0.05, 0.7, 'ひ\nょ\nう', **kwargs)
    ax.text(0.05, 0.2, 'が\n', **kwargs)
    ax.axis('off')


def make_logo(figsize, maprect, textrect):
    """Make logo given fig size and axes positions."""
    fig = plt.figure(figsize=figsize)
    if maprect is not None:
        draw_map(fig, maprect)
    if textrect is not None:
        draw_text(fig, textrect)
    return fig


def main():
    """Main program called during execution."""

#    # 1:1 with big map only (favicon)
#    fig = make_logo((9.6, 9.6), [0, 0, 1, 1], None)
#    fig.patch.set_facecolor('none')
#    fig.savefig(__file__[:-3]+'_favicon')

#    # 1:1 with small text
#    fig = make_logo((9.6, 9.6), [0.15, 0.15, 0.8, 0.8], [0.05, 0.05, 0.15, 0.3])
#    fig.savefig(__file__[:-3]+'_1x1')

#    # 1:3 with cropped map and text
#    fig = make_logo((9.6, 3.2), [1/6, -0.5, 1, 3], [0.1*1/4, 0.1, 1/4, 0.6])
#    fig.savefig(__file__[:-3]+'_1x3')
#    fig.savefig(__file__[:-3]+'_1x3.svg')

#    # 2:3 with big map and big text
#    fig = make_logo((9.6, 6.4), [1/3, 0.1, 2/3, 0.8], [0.1*2/3, 0.1, 1/3, 0.8])
#    fig.savefig(__file__[:-3]+'_2x3')
#    fig.savefig(__file__[:-3]+'_2x3.svg')
#
#    # 3:4 with big map and big text
#    fig = make_logo((9.6, 7.2), [1/4, 0.1, 3/4, 0.8], [0.1*3/4, 0.1, 1/4, 1/2])
#    fig.savefig(__file__[:-3]+'_3x4')
#
#    # 4:2 vertical map and text (3:1+1:1)
#    fig = make_logo((4.8, 9.6), [1/4, 5/8, 2/4, 2/8], [1/4, 1/8, 1/2, 4/8])
#    fig.savefig(__file__[:-3]+'_4x2')

#
    fig = make_logo((9.6, 3.2), [0.1, 0.1, 0.8, 0.8], None)
    ax = fig.add_axes([0, 0, 1, 1])
    bbox = ax.get_window_extent()
    height = bbox.height/fig.dpi*72
    kwargs = dict(fontsize=0.8*height, color='tab:blue')
    ax.text(0.35, 0.25, 'hy', ha='right', **kwargs)
    ax.text(0.65, 0.25, 'ga', ha='left', **kwargs)
    ax.axis('off')
    fig.savefig(__file__[:-3]+'_1x3')

def draw_text(fig, rect):
    """Draw logo japanese text."""
    plt.rc('font', family='TakaoPGothic')
    ax = fig.add_axes(rect)
    bbox = ax.get_window_extent()
    height = bbox.height/fig.dpi*72
    kwargs = dict(fontsize=0.4*height, va='center')
    ax.text(0.2, 0.7, '氷', **kwargs)
    ax.text(0.2, 0.2, '河', **kwargs)
    kwargs = dict(fontsize=0.05*height, linespacing=1.5, va='center')
    ax.text(0.05, 0.7, 'ひ\nょ\nう', **kwargs)
    ax.text(0.05, 0.2, 'が\n', **kwargs)
    ax.axis('off')
    fig.savefig(__file__[:-3]+'_1x1')


if __name__ == '__main__':
    main()
