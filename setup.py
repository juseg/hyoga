#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Build script for pismx."""

import setuptools

with open('README.rst', 'r') as f:
    README = f.read()

setuptools.setup(
    name='pismx',
    version='0.0',
    author='Julien Seguinot',
    description='A thin wrapper around xarray to open PISM files',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='http://github.com/juseg/pismx',
    license='gpl-3.0',
    install_requires=['xarray'],
    py_modules=['pismx'],
)
