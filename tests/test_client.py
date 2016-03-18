# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test client."""

from __future__ import absolute_import, print_function

import socket
import ssl

import httpretty
import pytest
from helpers import APIURL, get_client
from mock import patch
from requests import ConnectionError

from datacite import DataCiteMDSClient
from datacite.errors import HttpError as DataCiteHttpError


def test_api_url():
    """Test client init."""
    c = DataCiteMDSClient(
        username="TEST",
        prefix="10.1234",
        url="https://mds.example.org",  # without slash
        test_mode=True,
    )
    assert c.api_url == "https://mds.example.org/"  # with slash
    assert c.prefix == "10.1234"
    assert c.test_mode is True
    assert c.__repr__() == "<DataCiteMDSClient: TEST>"


@patch("datacite.request.requests")
def test_connection_error(requests):
    """Test connection error."""
    requests.get.side_effect = ConnectionError()

    c = get_client()
    with pytest.raises(DataCiteHttpError):
        c.doi_get("10.1234/foo.bar")


@patch("datacite.request.requests")
def test_ssl_error(requests):
    """Test HTTP error."""
    requests.get.side_effect = ssl.SSLError("The read operation timed out.")

    c = get_client()
    with pytest.raises(DataCiteHttpError):
        c.doi_get("10.1234/foo.bar")


@httpretty.activate
def test_timeout():
    """Test timeouts."""
    def callback(request, uri, headers):
        raise socket.timeout("timeout")

    httpretty.register_uri(
        httpretty.GET,
        "{0}doi/10.1234/1".format(APIURL),
        body=callback,
    )

    d = get_client(timeout=0.1)
    with pytest.raises(DataCiteHttpError):
        d.doi_get("10.1234/1")
