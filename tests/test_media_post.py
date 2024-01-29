# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for /media POST."""

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
def test_media_post_200():
    """Test."""
    responses.add(
        responses.POST,
        "{0}media/10.1234/1".format(APIURL),
        body="OK",
        status=200,
    )

    d = get_client()
    assert "OK" == d.media_post(
        "10.1234/1",
        {
            "text/plain": "http://example.org/text",
            "application/json": "http://example.org/json",
        },
    )
    assert (
        responses.calls[0].request.headers["content-type"] == "text/plain;charset=UTF-8"
    )
    lines = filter(lambda x: x, responses.calls[0].request.body.splitlines())
    assert len(list(lines)) == 2


@responses.activate
def test_media_post_400():
    """Test."""
    responses.add(
        responses.POST,
        "{0}media/10.1234/1".format(APIURL),
        body="Bad Request",
        status=400,
    )

    d = get_client()
    with pytest.raises(DataCiteBadRequestError):
        d.media_post("10.1234/1", {"text/plain": "http://invaliddomain.org"})


@responses.activate
def test_media_post_401():
    """Test."""
    responses.add(
        responses.POST,
        "{0}media/10.1234/1".format(APIURL),
        body="Unauthorized",
        status=401,
    )

    d = get_client()
    with pytest.raises(DataCiteUnauthorizedError):
        d.media_post("10.1234/1", {"text/plain": "http://example.org"})


@responses.activate
def test_media_post_403():
    """Test."""
    responses.add(
        responses.POST,
        "{0}media/10.1234/1".format(APIURL),
        body="Forbidden",
        status=403,
    )

    d = get_client()
    with pytest.raises(DataCiteForbiddenError):
        d.media_post("10.1234/1", {"text/plain": "http://example.org"})


@responses.activate
def test_media_post_500():
    """Test."""
    responses.add(
        responses.POST,
        "{0}media/10.1234/1".format(APIURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_client()
    with pytest.raises(DataCiteServerError):
        d.media_post("10.1234/1", {"text/plain": "http://example.org"})
