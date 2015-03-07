#!/usr/bin/env python
"""
    Jean-Lou Dupont's SSDP scripts
    
    Created on 2015-02-28
    @author: jldupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.2"

DESC="""
Overview
--------

Collection of SSDP related scripts

* jldssdp-discover:  listen for SSDP NOTIFY messages
* jldssdp-notify:    send SSDP NOTIFY message, optionally in a loop with delay
"""


from distutils.core import setup
from setuptools import find_packages


setup(name=         'jldssdp',
      version=      __version__,
      description=  'Collection of SSDP related tools',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'https://github.com/jldupont/jldssdp',
      package_dir=  {'': "src",},
      packages=     find_packages("src"),
      scripts=      ['src/scripts/jldssdp-discover'
                     ,'src/scripts/jldssdp-notify',
                     ],
      zip_safe=False
      ,long_description=DESC
      ,install_requires=[ "argparse", "twisted", "netifaces"
                         ]
      )

#############################################

f=open("latest", "w")
f.write(str(__version__)+"\n")
f.close()

