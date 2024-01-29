# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /media GET."""

import pytest
import responses
from helpers import APIURL, get_client

from datacite.errors import (
    DataCiteForbiddenError,
    DataCiteNotFoundError,
    DataCiteServerError,
    DataCiteUnauthorizedError,
)


@responses.activate
def test_media_get_200():
    """Test."""
    responses.add(
        responses.GET,
        "{0}media/10.1234/1".format(APIURL),
        body="application/json=http://example.org/json\r\n"
        "text/plain=http://example.org/text\r\n",
        status=200,
    )

    d = get_client()
    assert d.media_get("10.1234/1") == {
        "application/json": "http://example.org/json",
        "text/plain": "http://example.org/text",
    }


@responses.activate
def test_media_get_401():
    """Test."""
    responses.add(
        responses.GET,
        "{0}media/10.1234/1".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.media_get("10.1234/1")


@responses.activate
def test_media_get_403():
    """Test."""
    responses.add(
        responses.GET,
        "{0}media/10.1234/1".format(APIURL),
        body="login problem or dataset belongs to another party",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.media_get("10.1234/1")


@responses.activate
def test_media_get_404():
    """Test."""
    responses.add(
        responses.GET,
        "{0}media/10.1234/1".format(APIURL),
        body="Not Found",
        status=404,
    )

    d = get_client()
    with pytest.raises(DataCiteNotFoundError):
        d.media_get("10.1234/1")


@responses.activate
def test_media_get_500():
    """Test."""
    responses.add(
        responses.GET,
        "{0}media/10.1234/1".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.media_get("10.1234/1")
