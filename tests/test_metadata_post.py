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

import pytest
import responses
from helpers import APIURL, get_client

from datacite.errors import (
    DataCiteBadRequestError,
    DataCiteForbiddenError,
    DataCiteServerError,
    DataCiteUnauthorizedError,
)


@responses.activate
def test_metadata_post_201():
    """Test."""
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="OK",
        status=201,
    )

    d = get_client()
    assert "OK" == d.metadata_post("<resource></resource>")
    assert (
        responses.calls[0].request.headers["content-type"]
        == "application/xml;charset=UTF-8"
    )


@responses.activate
def test_metadata_post_400():
    """Test."""
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="Bad Request",
        status=400,
    )

    d = get_client()
    with pytest.raises(DataCiteBadRequestError):
        d.metadata_post("notxml")


@responses.activate
def test_metadata_post_401():
    """Test."""
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.metadata_post("notxml")


@responses.activate
def test_metadata_post_403():
    """Test."""
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.metadata_post("<resource></resource>")


@responses.activate
def test_metadata_post_500():
    """Test."""
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.metadata_post("<resource></resource>")
