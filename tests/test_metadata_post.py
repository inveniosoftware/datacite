# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /metadata POST."""

from __future__ import absolute_import, print_function

import pytest
from helpers import APIURL, get_client
from httpretty_mock import httpretty

from datacite.errors import DataCiteBadRequestError, DataCiteForbiddenError, \
    DataCiteServerError, DataCiteUnauthorizedError


@httpretty.activate
def test_metadata_post_201():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}metadata".format(APIURL),
        body="CREATED",
        status=201,
        location="http://example.org",
    )

    d = get_client(test_mode=True)
    assert "CREATED" == d.metadata_post("<resource></resource>")
    assert httpretty.last_request().headers['content-type'] == \
        "application/xml;charset=UTF-8"
    assert httpretty.last_request().querystring['testMode'] == ["1"]


@httpretty.activate
def test_metadata_post_400():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}metadata".format(APIURL),
        body="Bad Request",
        status=400,
    )

    d = get_client()
    with pytest.raises(DataCiteBadRequestError):
        d.metadata_post("notxml")


@httpretty.activate
def test_metadata_post_401():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}metadata".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.metadata_post("notxml")


@httpretty.activate
def test_metadata_post_403():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}metadata".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.metadata_post("<resource></resource>")


@httpretty.activate
def test_metadata_post_500():
    """Test."""
    httpretty.register_uri(
        httpretty.POST,
        "{0}metadata".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.metadata_post("<resource></resource>")
