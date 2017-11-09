# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /metadata GET."""

from __future__ import absolute_import, print_function

import pytest
from helpers import APIURL, get_client
from httpretty_mock import httpretty

from datacite.errors import DataCiteForbiddenError, DataCiteGoneError, \
    DataCiteNotFoundError, DataCiteServerError, DataCiteUnauthorizedError


@httpretty.activate
def test_metadata_get_200():
    """Test."""
    doc = "<resource></resource>"
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body=doc,
        status=200,
        content_type="application/xml",
    )

    d = get_client()
    assert doc == d.metadata_get("10.1234/1")


@httpretty.activate
def test_metadata_get_401():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.metadata_get("10.1234/1")


@httpretty.activate
def test_metadata_get_403():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.metadata_get("10.1234/1")


@httpretty.activate
def test_metadata_get_404():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body="Not Found",
        status=404,
    )

    d = get_client()
    with pytest.raises(DataCiteNotFoundError):
        d.metadata_get("10.1234/1")


@httpretty.activate
def test_metadata_get_410():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body="Gone",
        status=410,
    )

    d = get_client()
    with pytest.raises(DataCiteGoneError):
        d.metadata_get("10.1234/1")


@httpretty.activate
def test_metadata_get_500():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}metadata/10.1234/1".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.metadata_get("10.1234/1")
