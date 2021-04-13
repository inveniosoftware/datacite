#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
# Copyright (C) 2015-2020 CERN.
#
# Datacite is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Run tests with real HTTP calls to Datacite REST APIs to their test endpoint.

# Quit on errors
set -o errexit

if [ -z "${DATACITE_USER}" ] || [ -z "${DATACITE_PW}" ] || [ -z "${DATACITE_PREFIX}" ]; then
  echo "DATACITE_USER, DATACITE_PW or DATACITE_PREFIX env var not set"
  exit 1
fi

python -m pytest --runpw
