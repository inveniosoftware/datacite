# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test documentation example."""

import responses

APIURL = "https://mds.test.datacite.org/"


@responses.activate
def test_example():
    """Test documentation example."""
    doi = "10.1234/test-doi"
    url = "http://example.org/test-doi"

    # metadata post
    responses.add(
        responses.POST,
        "{0}metadata".format(APIURL),
        body="CREATED",
        status=201,
    )

    # doi post
    responses.add(
        responses.POST,
        "{0}doi".format(APIURL),
        body="CREATED",
        status=201,
    )

    # doi get
    responses.add(
        responses.GET,
        "{0}doi/{1}".format(APIURL, doi),
        body=url,
        status=200,
    )

    # media post
    responses.add(
        responses.POST,
        "{0}media/{1}".format(APIURL, doi),
        body="OK",
        status=200,
    )

    # media get
    responses.add(
        responses.GET,
        "{0}media/{1}".format(APIURL, doi),
        body="application/json=http://example.org/test-doi/json/\r\n"
        "application/xml=http://example.org/test-doi/xml/\r\n",
        status=200,
    )

    # metadata get
    responses.add(
        responses.GET,
        "{0}metadata/{1}".format(APIURL, doi),
        body="<resource>...</resource>",
        status=200,
        content_type="application/xml",
    )

    # metadata delete
    responses.add(
        responses.DELETE,
        "{0}metadata/{1}".format(APIURL, doi),
        body="OK",
        status=200,
    )

    import example.full

    assert example.full.location == url
    assert example.full.doc == "<resource>...</resource>"
