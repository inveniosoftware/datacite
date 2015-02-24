# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

# Use Python-2.7 image:
FROM python:2.7

# Install some prerequisites ahead of `setup.py` in order to profit
# from the docker build cache:
RUN pip install "coverage<4.0a1" \
                docutils \
                httpretty \
                jinja2 \
                markupsafe \
                mock \
                pep257 \
                pytest \
                pytest-cache \
                pytest-cov \
                pytest-pep8 \
                requests \
                sphinx \
                sphinx-rtd-theme

# Add sources to `/code` and work there:
ADD . /code
WORKDIR /code

# Install DataCite:
RUN pip install -e .[docs]

# Run container as user `datacite` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' datacite && \
    chown -R datacite:datacite /code
USER datacite

# Run PEP-257 check and build documentation:
RUN pep257 datacite
RUN python setup.py build_sphinx

# Run test suite instead of starting the application:
CMD ["python", "setup.py", "test"]
