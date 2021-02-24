# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Sphinx configuration file for hyoga documentation."""

# -- Project information -----------------------------------------------------

project = 'hyoga'
copyright = '2021, Julien Seguinot'
author = 'Julien Seguinot'


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
    ]

# options to sphinx extensions
autosummary_generate = True         # autogen files for listed entroes
sphinx_gallery_conf = {
    'examples_dirs': '../examples', # path to example scripts
    'gallery_dirs': 'examples',     # where to save gallery plots
    }

# location of additional templates
# templates_path = ['_templates']

# patterns to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# sphinx html theme
html_theme = 'sphinx_rtd_theme'

# static files copied to build (e.g. default.css)
# html_static_path = ['_static']
