# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

# docker build .
FROM python:3.4
RUN pip install pep257 "coverage<4.0a1"
RUN pip install pytest pytest-pep8 pytest-cov pytest-cache
RUN pip install mock httpretty requests
RUN pip install sphinx_rtd_theme
ADD . /code
WORKDIR /code
RUN pip install -e .
RUN pep257 datacite
RUN sphinx-build -qnNW docs docs/_build/html
RUN python setup.py test
