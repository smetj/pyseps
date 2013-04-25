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

import setuptools
import inspect
from os import path
from sys import version_info

PROJECT = 'pyseps'
VERSION = '0.1'

#The goal is to have a .pth file so it can be included when creating RPMs
module_path=path.dirname((path.dirname(inspect.getfile(setuptools))))
pth_dir="./%s-%s-py%s.egg"%(PROJECT,
    VERSION,
    '.'.join(str(i) for i in version_info[0:2]))
pth=open ("%s/%s.pth"%(module_path,PROJECT),'w')
pth.write(pth_dir)
pth.close()


setuptools.setup(
    name=PROJECT,
    version=VERSION,
    description="A PYthon Simple Event Procsessing System.",
    author="Jelle Smet",
    url="https://github.com/smetj/pyseps",
    install_requires=['wishbone'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
        'pyseps = pyseps.pyseps:main'
        ],

    'pyseps.module': [
                'TailingCursor=pyseps.tailingcursor:TailingCursor',
                'MapMatch=pyseps.mapmatch:MapMatch'
        ],
    }
)
