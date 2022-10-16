# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Sphinx configuration file for hyoga documentation."""


import sphinx_autosummary_accessors
import sphinx_gallery.sorting


# -- Project information -----------------------------------------------------

project = 'hyoga'
copyright = '2021-2022'
author = 'Julien Seguinot'
version = '0.1 Akaishi'
release = '0.1.2'


# -- General configuration ---------------------------------------------------

templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'


# -- Sphinx extensions -------------------------------------------------------

# sphinx extensions
extensions = [
    'matplotlib.sphinxext.plot_directive',  # make plots from code
    'sphinx.ext.autodoc',       # make docs from dosctrings
    'sphinx.ext.autosummary',   # each entry on a different page
    'sphinx.ext.extlinks',      # external links e.g. github
    'sphinx.ext.intersphinx',   # link to other projects
    'sphinx.ext.napoleon',      # numpy-style docstrings
    'sphinx_autosummary_accessors',  # autosummary Dataset.hyoga.etc
    'sphinx_gallery.gen_gallery',    # plotting examples gallery
    ]

# configure matplotlib plot directive
plot_formats = [('png', 100), ('pdf', 100)]  # no hires.png
plot_include_source = True          # show source code by default
plot_html_show_source_link = False  # no link to py script file
plot_html_show_formats = False      # no link to output images

# configure sphinx.ext.autosummary
autosummary_generate = True         # autogen files for listed entroes

# configure sphinx.ext.extlinks
extlinks = {
    "issue": ("https://github.com/juseg/hyoga/issues/%s", "#%s"),
    "pull": ("https://github.com/juseg/hyoga/pull/%s", "PR%s"),
}

# configure sphinx.ext.intersphinx
intersphinx_mapping = {
    'geopandas': ('https://geopandas.org/en/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'python': ('https://docs.python.org/3.7/', None),
    'xarray': ('http://xarray.pydata.org/en/stable/', None)
}

# configure sphinx.ext.napoleon
napoleon_use_param = True           # add :param: roles to parameters
napoleon_use_rtype = False          # do not show return type
napoleon_preprocess_types = True    # appears needed by aliases
napoleon_type_aliases = {
    # general terms (https://docs.python.org/3/glossary.html)
    'callable': ':py:func:`callable`',
    'file-like': ':term:`file-like <file-like object>`',
    'iterable': ':term:`iterable`',
    'mapping': ':term:`mapping`',
    'sequence': ':term:`sequence`',
    # object shortcuts
    'Axes': '~matplotlib.axes.Axes',
    'AxesImage': '~matplotlib.image.AxesImage',
    'CRS': '~cartopy.crs.CRS',
    'GeoAxes': '~cartopy.mpl.geoaxes.GeoAxes',
    'GeoDataFrame': '~geopandas.GeoDataFrame',
    'QuadContourSet': '~matplotlib.contour.QuadContourSet',
    'StreamplotSet': '~matplotlib.streamplot.StreamplotSet',
    'DataArray': '~xarray.DataArray',
    'Dataset': '~xarray.Dataset',
    'Path': '~~pathlib.Path',
}

# configure sphinx_gallery.gen_gallery
sphinx_gallery_conf = {
    'examples_dirs': '../examples',  # path to example scripts
    'gallery_dirs': 'examples',      # where to save gallery plots
    # 'nested_sections' : False,     # fix duplicate sub-headings in rtd theme
    'subsection_order': sphinx_gallery.sorting.ExplicitOrder([
        '../examples/showcase',
        '../examples/interp',
        '../examples/cartography'])
    }


# -- Options for HTML output -------------------------------------------------

# sphinx html logo
html_logo = '_static/png/hyoga_logo.png'

# sphinx html theme
html_theme = 'sphinx_book_theme'
html_theme_options = {
    'logo_only': True,
    'repository_url': 'https://github.com/juseg/hyoga',
    'repository_branch': 'main',
    'use_download_button': True,
    'use_edit_page_button': True,
    'use_fullscreen_button': True,
    'use_issues_button': False,
    'use_repository_button': True,
    'logo_only': True,
    'extra_navbar': None,
    'extra_footer': (
        'Currently developed within a '
        '<a href="https://mohnfoundation.no/en/">Trond Mohn Foundation</a> '
        '<a href="https://mountainsinmotion.w.uib.no">project</a> at the '
        '<a href="https://www.uib.no/en">University of Bergen</a>.'),
    'toc_title': 'Page contents'}

# static files copied to build
html_static_path = ['_static']
html_css_files = ['css/custom.css']
