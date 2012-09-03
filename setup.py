#!/usr/bin/env python

import os
from distutils.core import setup
from eventlib import __version__

def find_packages(toplevel):
    return [directory.replace(os.path.sep, '.') for directory, subdirs, files in os.walk(toplevel) if '__init__.py' in files]

setup(name='python-eventlib',
      version=__version__,
      description='Coroutine-based networking library',
      author='Linden Lab',
      maintainer="AG Projects",
      maintainer_email="support@ag-projects.com",
      url='http://devel.ag-projects.com/repositories/python-eventlib',
      packages=find_packages('eventlib'),
      long_description="""
        Eventlib is a networking library written in Python. It achieves
        high scalability by using non-blocking io while at the same time
        retaining high programmer usability by using coroutines to make
        the non-blocking io operations appear blocking at the source code
        level.""",
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Operating System :: MacOS :: MacOS X",
      "Operating System :: POSIX",
      "Topic :: Internet",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Intended Audience :: Developers",
      "Development Status :: 4 - Beta"
    ])

