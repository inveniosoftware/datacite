# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /doi POST."""

from __future__ import absolute_import, print_function

import pytest
from helpers import APIURL, get_client
from httpretty_mock import httpretty

from datacite._compat import b
from datacite.errors import DataCiteBadRequestError, DataCiteForbiddenError, \
    DataCitePreconditionError, DataCiteServerError, \
    DataCiteUnauthorizedError


@httpretty.activate
def test_doi_post_200():
    """Test."""
    doi = "10.1234/1"
    url = "http://example.org"

    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="CREATED",
        status=201,
    )

    d = get_client()
    assert "CREATED" == d.doi_post(doi, url)
    assert httpretty.last_request().headers['content-type'] == \
        "text/plain;charset=UTF-8"
    assert httpretty.last_request().body == \
        b("doi={0}\r\nurl={1}".format(doi, url))


@httpretty.activate
def test_doi_post_400():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="Bad Request",
        status=400,
    )

    d = get_client()
    with pytest.raises(DataCiteBadRequestError):
        d.doi_post("baddoi", "http://invaliddomain.org")


@httpretty.activate
def test_doi_post_401():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.doi_post("10.1234/1", "http://example.org")


@httpretty.activate
def test_doi_post_403():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.doi_post("10.1234/1", "http://example.org")


@httpretty.activate
def test_doi_post_412():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="Precondition failed",
        status=412,
    )

    d = get_client(test_mode=True)
    with pytest.raises(DataCitePreconditionError):
        d.doi_post("10.1234/1", "http://example.org")

    assert httpretty.last_request().querystring['testMode'] == ["1"]


@httpretty.activate
def test_doi_post_500():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}doi".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.doi_post("10.1234/1", "http://example.org")
