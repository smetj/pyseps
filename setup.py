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
import re
import ast

###############################################################
PROJECT = 'pyseps'
MODULE = 'MapMatch'
VERSION = "0.3.0"
FILE = "pyseps/mapmatch.py"
AUTHOR = "Jelle Smet"
URL='https://github.com/smetj/pyseps'
INSTALL_REQUIRES= [ 'wishbone','gevent_inotifyx','PyYAML' ]
ENTRY_POINTS={
    "pyseps": "mapmatch = pyseps:MapMatch"
}
###############################################################

m = ast.parse(''.join(open(FILE)))
for node in m.body:
    if isinstance(node, ast.ClassDef) and node.name == MODULE:
            DOCSTRING=ast.get_docstring(node)

try:
    with open ("README.md", "w") as readme:
        readme.write(PROJECT+"\n")
        readme.write("="*len(PROJECT)+"\n\n")
        readme.write("version: %s\n\n"%(VERSION))
        readme.write(DOCSTRING+"\n")
except:
    pass

try:
    with open('README.md') as readme:
        long_description = readme.read()
except:
    long_description=''

setuptools.setup(
    name=PROJECT,
    version=VERSION,
    description=re.search(".*?\*\*(.*?)\*\*",DOCSTRING).group(1),
    long_description=long_description,
    author=AUTHOR,
    url=URL,
    install_requires=[ "wishbone" ] + INSTALL_REQUIRES,
    packages=setuptools.find_packages(),
    zip_safe=True,
    entry_points=ENTRY_POINTS,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators',
                 ],
)