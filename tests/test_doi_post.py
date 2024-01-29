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

import pytest
import responses
from helpers import APIURL, get_client

from datacite.errors import (
    DataCiteBadRequestError,
    DataCiteForbiddenError,
    DataCitePreconditionError,
    DataCiteServerError,
    DataCiteUnauthorizedError,
)


@responses.activate
def test_doi_post_200():
    """Test."""
    doi = "10.1234/1"
    url = "http://example.org"

    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="CREATED",
        status=201,
    )

    d = get_client()
    assert "CREATED" == d.doi_post(doi, url)
    assert (
        responses.calls[0].request.headers["content-type"] == "text/plain;charset=UTF-8"
    )
    expected_response = "doi={0}\r\nurl={1}".format(doi, url).encode("utf8")
    assert responses.calls[0].request.body == expected_response


@responses.activate
def test_doi_post_400():
    """Test."""
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="Bad Request",
        status=400,
    )

    d = get_client()
    with pytest.raises(DataCiteBadRequestError):
        d.doi_post("baddoi", "http://invaliddomain.org")


@responses.activate
def test_doi_post_401():
    """Test."""
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.doi_post("10.1234/1", "http://example.org")


@responses.activate
def test_doi_post_403():
    """Test."""
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.doi_post("10.1234/1", "http://example.org")


@responses.activate
def test_doi_post_412():
    """Test."""
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="Precondition failed",
        status=412,
    )

    d = get_client()
    with pytest.raises(DataCitePreconditionError):
        d.doi_post("10.1234/1", "http://example.org")


@responses.activate
def test_doi_post_500():
    """Test."""
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.doi_post("10.1234/1", "http://example.org")
