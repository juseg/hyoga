# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Sphinx configuration file for hyoga documentation."""


import sphinx_autosummary_accessors
import sphinx_gallery.sorting

# -- Project information -----------------------------------------------------

project = 'hyoga'
copyright = '2021, Julien Seguinot'
author = 'Julien Seguinot'
version = '0.1 Akaishi'
release = '0.1.1'


# -- General configuration ---------------------------------------------------

# sphinx extensions
extensions = [
    'sphinx.ext.autodoc',       # make docs from dosctrings
    'sphinx.ext.autosummary',   # each entry on a different page
    'sphinx.ext.intersphinx',   # link to other projects
    'sphinx.ext.extlinks',      # external links e.g. github
    'sphinx.ext.napoleon',      # numpy-style docstrings
    'sphinx_gallery.gen_gallery',           # plotting examples gallery
    'IPython.sphinxext.ipython_directive',  # run code samples and plots
    'IPython.sphinxext.ipython_console_highlighting',
    'sphinx_autosummary_accessors', # autosummary Dataset.hyoga.etc
    ]

# options to sphinx extensions
autosummary_generate = True         # autogen files for listed entroes
sphinx_gallery_conf = {
    'examples_dirs': '../examples',  # path to example scripts
    'gallery_dirs': 'examples',     # where to save gallery plots
    'subsection_order': sphinx_gallery.sorting.ExplicitOrder([
        '../examples/showcase',
        '../examples/interp'])
    }
extlinks = {
    "issue": ("https://github.com/pydata/xarray/issues/%s", "#%s"),
    "pull": ("https://github.com/pydata/xarray/pull/%s", "PR%s"),
}
intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'python': ('https://docs.python.org/3.7/', None),
    'xarray': ('http://xarray.pydata.org/en/stable/', None)
}
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
    'QuadContourSet': '~matplotlib.contour.QuadContourSet',
    'StreamplotSet': '~matplotlib.streamplot.StreamplotSet',
    'DataArray': '~xarray.DataArray',
    'Dataset': '~xarray.Dataset',
    'Path': '~~pathlib.Path',
}

# location of additional templates
templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]

# patterns to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# sphinx html theme
html_theme = 'sphinx_rtd_theme'

# static files copied to build (e.g. default.css)
# html_static_path = ['_static']
