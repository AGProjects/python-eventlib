#!/usr/bin/python2

import os

from distutils.core import setup
from eventlib import __version__


def find_packages(toplevel):
    return [directory.replace(os.path.sep, '.') for directory, subdirs, files in os.walk(toplevel) if '__init__.py' in files]


setup(
    name='python-eventlib',
    version=__version__,

    description='Coroutine-based networking library',
    url='http://devel.ag-projects.com/repositories/python-eventlib',

    author='Linden Lab',
    maintainer="AG Projects",
    maintainer_email="support@ag-projects.com",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],

    packages=find_packages('eventlib')
)
