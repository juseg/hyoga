#!/usr/bin/env python
# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Build script for cartowik."""

import setuptools

with open('README.rst', 'r') as f:
    README = f.read()

setuptools.setup(
    name='cartowik',
    version='0.0.0',
    author='Julien Seguinot',
    author_email='seguinot@vaw.baug.ethz.ch',
    description='Draw Wikipedia style location and topographic maps',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='http://github.com/juseg/cartowik',
    license='gpl-3.0',
    packages=setuptools.find_packages(),
    install_requires=['cartopy', 'matplotlib'],
)
