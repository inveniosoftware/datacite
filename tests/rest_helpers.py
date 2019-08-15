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

from datacite import DataCiteRESTClient


def get_rest(username="DC", password="pw",
             test_mode=True, timeout=None):
    """Create a API client."""
    return DataCiteRESTClient(
        username=username,
        password=password,
        test_mode=test_mode,
        timeout=timeout,
    )
