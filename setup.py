#!/usr/bin/env python
# Copyright (c) 2019-2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Build script for hyoga."""

import setuptools

with open('README.rst', 'r') as f:
    README = f.read()

setuptools.setup(
    name='hyoga',
    version='0.0',
    author='Julien Seguinot',
    description='A thin wrapper around xarray to open and plot PISM files',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='http://github.com/juseg/hyoga',
    license='gpl-3.0',
    install_requires=['xarray'],
    py_modules=['hyoga'],
)
