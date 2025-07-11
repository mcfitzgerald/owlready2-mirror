#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Owlready2
# Copyright (C) 2013-2018 Jean-Baptiste LAMY

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, os.path, sys, glob

# get a canonical representation of relative path of the directory of this file
#HERE = os.path.relpath(os.path.dirname(os.path.abspath(sys.modules.get(__name__).__file__)))
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) <= 1: sys.argv.append("install")

import setuptools

version = open(os.path.join(HERE, "__init__.py")).read().split('VERSION = "', 1)[1].split('"', 1)[0]

def do_setup(extensions):
  return setuptools.setup(
  #name         = "Owlready2",
  name         = "owlready2",
  version      = version,
  description  = "A package for ontology-oriented programming in Python: load OWL 2.0 ontologies as Python objects, modify them, save them, and perform reasoning via HermiT. Includes an optimized RDF quadstore.",
  long_description = open(os.path.join(HERE, "README.rst")).read(),
  # license      = "LGPLv3+",
  # author       = "Lamy Jean-Baptiste (Jiba)",
  # author_email = "jibalamy@free.fr",
  # url          = "https://bitbucket.org/jibalamy/owlready2",
  
  package_dir  = {"owlready2" : HERE},
  packages     = ["owlready2", "owlready2.pymedtermino2", "owlready2.sparql"],
  package_data = {"owlready2" : ["owlready_ontology.owl",
                                 "ontos/*.owl",
                                 "hermit/*.*", "hermit/org/semanticweb/HermiT/*", "hermit/org/semanticweb/HermiT/cli/*", "hermit/org/semanticweb/HermiT/hierarchy/*",
                                 "pellet/*.*", "pellet/org/mindswap/pellet/taxonomy/printer/*",
                                ]},
  
  ext_modules = extensions,
)

try:
  import Cython.Build
  extensions = [
    setuptools.Extension("owlready2_optimized", ["owlready2_optimized.pyx"]),
  ]
  extensions = Cython.Build.cythonize(extensions, compiler_directives = { "language_level" : 3 })
  dist = do_setup(extensions)
except:
  dist = do_setup([])

  

if len(sys.argv) >= 2 and sys.argv[1] == "develop":
    # `python setup.py develop` (and `pip install -e .`) assumes a directory structure
    # where the package to be installed lives in a subirectory.
    # However, to maintain backward compatibility, this package is structured
    # differently. To allow `python setup.py develop` anyway, we do some manual
    # tweaks.

    # Note: relative import not possible here due to PEP 338
    # Thus, we use an absolute import assuming that the name is unique
    # noinspection PyUnresolvedReferences
    from setup_develop_mode import install_develop_mode
    install_develop_mode(dist)
