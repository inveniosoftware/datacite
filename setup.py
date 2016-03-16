# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Python API wrapper for the DataCite Metadata Store API."""

import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

install_requires = [
    'jsonschema>=2.5.1',
    'lxml>=3.5.0',
    'requests>=2.3',
]

tests_require = [
    'coverage<4.0a1',
    'httpretty>=0.8.0',
    'mock>=1.0',
    'pydocstyle>=1.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest-runner>=2.6.2',
    'pytest>=2.6.1',
]

docs_require = {
    'sphinx_rtd_theme',
}

extras_require = {
        'docs': docs_require,
        'tests': tests_require,
}

# Get the version string.  Cannot be done with import!
with open(os.path.join('datacite', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

setup(
    name='datacite',
    version=version,
    description=__doc__,
    author='Invenio Collaboration',
    author_email='info@invenio-software.org',
    url='https://github.com/inveniosoftware/datacite',
    packages=['datacite'],
    zip_safe=False,
    extras_require=extras_require,
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
