#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "Plinx"
DESCRIPTION = "Plinx is an experimental, minimalistic, and extensible web framework and ORM written in Python."
URL = "https://github.com/dhavalsavalia/plinx"
EMAIL = "coder@dhavalsavalia.com"
AUTHOR = "Dhaval Savalia"
REQUIRES_PYTHON = ">=3.11.0"
VERSION = None

REQUIRED = ["webob", "parse", "requests", "requests-wsgi-adapter"]
EXTRAS = {}

with open("VERSION", "r") as f:
    VERSION = f.read().strip()

# Below is from setup.py for humans (https://github.com/navdeep-G/setup.py)
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
about["__version__"] = VERSION



# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    setup_requires=["wheel"],
)
