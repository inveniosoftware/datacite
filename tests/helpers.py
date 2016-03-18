# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test helpers."""

from __future__ import absolute_import, print_function

from datacite import DataCiteMDSClient

APIURL = "https://mds.example.org/"


def get_client(username="DC", password="pw", prefix='10.5072',
               test_mode=False, timeout=None):
    """Create a API client."""
    return DataCiteMDSClient(
        username=username,
        password=password,
        prefix=prefix,
        url=APIURL,
        test_mode=test_mode,
        timeout=timeout,
    )
