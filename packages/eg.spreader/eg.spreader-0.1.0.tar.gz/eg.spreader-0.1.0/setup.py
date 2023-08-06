"""
spreader.py setup file

Copyright (c) 2022, Eugene Gershnik
SPDX-License-Identifier: BSD-3-Clause
"""

from skbuild import setup  
from pathlib import Path
import platform
import sys

mydir = Path(__file__).parent

README = (mydir/"README.md").read_text()

CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: POSIX :: BSD
Programming Language :: C++
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Topic :: Software Development
Topic :: Office/Business :: Financial :: Spreadsheet 
Typing :: Typed 
""".splitlines()

CMAKE_EXTRA_ARGS = []

pythonType = platform.python_implementation()
system = platform.system()

#work around bug in scikit-build
if system == 'Windows' and pythonType == 'PyPy':
    maj, min, _ = platform.python_version_tuple()
    CMAKE_EXTRA_ARGS += [f'-DPYTHON_LIBRARY={sys.base_prefix}/libs/python{maj}{min}.lib']

setup(
    name="eg.spreader",
    version="0.1.0",
    description="Fast spreadsheet logic library",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Eugene Gershnik',
    author_email='gershnik@hotmail.com',
    url="https://github.com/gershnik/spreader.py",
    download_url="http://pypi.python.org/pypi/spreader/",
    license="BSD-3-Clause",
    package_dir={'':'code/wrappers/python/src'},
    packages=['eg.spreader'],
    package_data = {
        'eg.spreader': ['py.typed'],
    },
    python_requires=">=3.7",

    cmake_source_dir="code",
    cmake_args= [
        '-DSPR_PYTHON_PACKAGE_DIR=code/wrappers/python/src/eg'
    ] + CMAKE_EXTRA_ARGS
)
