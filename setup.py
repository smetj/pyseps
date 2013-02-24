#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#  
#  Copyright 2013 Jelle Smet <development@smetj.net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

PROJECT = 'pyseps'

VERSION = '0.1'


from setuptools import setup, find_packages

from distutils.util import convert_path
from fnmatch import fnmatchcase
import os
import sys

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='A PYthon Simple Event Procsessing System',
    long_description=long_description,

    author='Jelle Smet',
    author_email='development@smetj.net',

    url='https://github.com/smetj/pyseps',
    download_url='https://github.com/smetj/pyseps/tarball/master',

    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: System Engineers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    
    entry_points={
        'console_scripts': [
		'pyseps = pyseps.pyseps:main'
        ],

	'pyseps.module': [
                'TailingCursor=pyseps.tailingcursor:TailingCursor'
        ],
    },

    zip_safe=False,
    )
