#!/usr/bin/env python
"""
    Jean-Lou Dupont's SSDP scripts
    
    Created on 2015-02-28
    @author: jldupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.1"

DESC="""
Overview
--------

Collection of SSDP related scripts

* jldssdp-discover:  listen for SSDP NOTIFY messages
"""


from distutils.core import setup
from setuptools import find_packages


setup(name=         'jldssdp',
      version=      __version__,
      description=  'Collection of SSDP related tools',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      #url=          'http://www.systemical.com/doc/opensource/jldzeromq',
      package_dir=  {'': "src",},
      packages=     find_packages("src"),
      scripts=      ['src/scripts/jldssdp-discover',
                     ],
      zip_safe=False
      ,long_description=DESC
      ,install_requires=[ "argparse", "twisted",
                         ]
      )

#############################################

f=open("latest", "w")
f.write(str(__version__)+"\n")
f.close()

