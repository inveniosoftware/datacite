# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /doi GET."""

from __future__ import absolute_import, print_function

import pytest
from helpers import APIURL, get_client
from httpretty_mock import httpretty

from datacite.errors import DataCiteForbiddenError, DataCiteGoneError, \
    DataCiteNoContentError, DataCiteNotFoundError, DataCiteServerError, \
    DataCiteUnauthorizedError


@httpretty.activate
def test_doi_get_200():
    """Test."""
    url = "http://example.org"
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body=url,
        status=200,
    )

    d = get_client()
    assert url == d.doi_get("10.1234/1")


@httpretty.activate
def test_doi_get_204():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="No Content",
        status=204,
    )

    d = get_client(test_mode=True)
    with pytest.raises(DataCiteNoContentError):
        d.doi_get("10.1234/1")

    assert httpretty.last_request().querystring['testMode'] == ["1"]


@httpretty.activate
def test_doi_get_401():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.doi_get("10.1234/1")


@httpretty.activate
def test_doi_get_403():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.doi_get("10.1234/1")


@httpretty.activate
def test_doi_get_404():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Not Found",
        status=404,
    )

    d = get_client()
    with pytest.raises(DataCiteNotFoundError):
        d.doi_get("10.1234/1")


@httpretty.activate
def test_doi_get_410():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Gone",
        status=410,
    )

    d = get_client()
    with pytest.raises(DataCiteGoneError):
        d.doi_get("10.1234/1")


@httpretty.activate
def test_doi_get_500():
    """Test."""
    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.doi_get("10.1234/1")
