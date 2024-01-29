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

import pytest
import responses
from helpers import APIURL, get_client

from datacite.errors import (
    DataCiteForbiddenError,
    DataCiteGoneError,
    DataCiteNoContentError,
    DataCiteNotFoundError,
    DataCiteServerError,
    DataCiteUnauthorizedError,
)


@responses.activate
def test_doi_get_200():
    """Test."""
    url = "http://example.org"
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body=url,
        status=200,
    )

    d = get_client()
    assert url == d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_204():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        status=204,
    )

    d = get_client()
    with pytest.raises(DataCiteNoContentError):
        d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_401():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_403():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_404():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Not Found",
        status=404,
    )

    d = get_client()
    with pytest.raises(DataCiteNotFoundError):
        d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_410():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Gone",
        status=410,
    )

    d = get_client()
    with pytest.raises(DataCiteGoneError):
        d.doi_get("10.1234/1")


@responses.activate
def test_doi_get_500():
    """Test."""
    responses.add(
        responses.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.doi_get("10.1234/1")
