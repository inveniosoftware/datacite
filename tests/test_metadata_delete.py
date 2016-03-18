# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /metadata DELETE."""

from __future__ import absolute_import, print_function

import httpretty
import pytest
from helpers import APIURL, get_client

from datacite.errors import DataCiteForbiddenError, DataCiteNotFoundError, \
    DataCiteServerError, DataCiteUnauthorizedError


@httpretty.activate
def test_metadata_delete_200():
    """Test."""
    httpretty.register_uri(
        httpretty.DELETE,
        "{0}metadata/10.1234/example".format(APIURL),
        body="OK",
        status=200,
    )

    d = get_client(test_mode=True)
    assert "OK" == d.metadata_delete("10.1234/example")
    assert httpretty.last_request().querystring['testMode'] == ["1"]


@httpretty.activate
def test_metadata_delete_401():
    """Test."""
    httpretty.register_uri(
        httpretty.DELETE,
        "{0}metadata/10.1234/example".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.metadata_delete("10.1234/example")


@httpretty.activate
def test_metadata_delete_403():
    """Test."""
    httpretty.register_uri(
        httpretty.DELETE,
        "{0}metadata/10.1234/example".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.metadata_delete("10.1234/example")


@httpretty.activate
def test_metadata_delete_404():
    """Test."""
    httpretty.register_uri(
        httpretty.DELETE,
        "{0}metadata/10.1234/example".format(APIURL),
        body="Not found",
        status=404,
    )

    d = get_client()
    with pytest.raises(DataCiteNotFoundError):
        d.metadata_delete("10.1234/example")


@httpretty.activate
def test_metadata_delete_500():
    """Test."""
    httpretty.register_uri(
        httpretty.DELETE,
        "{0}metadata/10.1234/example".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.metadata_delete("10.1234/example")
