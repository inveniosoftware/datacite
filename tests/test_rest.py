# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
# Copyright (C) 2020 Caltech.
# Copyright (C) 2021 Graz University of Technology.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for REST API."""

import pytest
import responses
from helpers import (
    RESTURL,
    TEST_43_JSON_FILES,
    TEST_45_JSON_FILES,
    get_credentials,
    get_rest,
    load_json_path,
)

from datacite.errors import (
    DataCiteForbiddenError,
    DataCiteGoneError,
    DataCiteNoContentError,
    DataCiteNotFoundError,
    DataCiteServerError,
    DataCiteUnauthorizedError,
)


@pytest.mark.pw
def test_rest_create_draft():
    username, password, prefix = get_credentials()
    d = get_rest(
        username=username, password=password, prefix=prefix, with_fake_url=False
    )
    doi = d.draft_doi()
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    url = "https://github.com/inveniosoftware/datacite"
    new_url = d.update_url(doi, url)
    assert new_url == url
    d.delete_doi(doi)


@pytest.mark.pw
def test_rest_create_draft_metadata():
    username, password, prefix = get_credentials()
    d = get_rest(
        username=username, password=password, prefix=prefix, with_fake_url=False
    )
    metadata = {"titles": [{"title": "hello world", "lang": "en"}]}
    doi = prefix + "/12345"
    returned_doi = d.draft_doi(metadata, doi)
    assert returned_doi == doi
    url = "https://github.com/inveniosoftware/datacite"
    returned_metadata = d.update_doi(doi, url=url)
    assert returned_metadata["url"] == url
    assert returned_metadata["titles"][0]["title"] == "hello world"
    d.delete_doi(doi)


@responses.activate
def test_rest_create_draft_mock():
    prefix = "10.1234"
    mock = "https://github.com/inveniosoftware/datacite"
    data = {"data": {"id": prefix + "/1", "attributes": {"url": mock}}}
    responses.add(
        responses.POST,
        "{0}dois".format(RESTURL),
        json=data,
        status=201,
    )
    d = get_rest(username="mock", password="mock", prefix=prefix)
    doi = d.draft_doi()
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix

    responses.add(
        responses.PUT,
        "{0}dois/10.1234/1".format(RESTURL),
        json=data,
        status=200,
    )
    new_url = d.update_url(doi, mock)
    assert new_url == mock

    responses.add(
        responses.DELETE,
        "{0}dois/10.1234/1".format(RESTURL),
        status=204,
    )
    d.delete_doi(doi)


@pytest.mark.parametrize("example_json43", TEST_43_JSON_FILES)
@pytest.mark.pw
def test_rest_create_public_43(example_json43):
    """Test creating DOIs with all example metadata"""
    example_metadata = load_json_path(example_json43)
    url = "https://github.com/inveniosoftware/datacite"
    username, password, prefix = get_credentials()
    d = get_rest(
        username=username, password=password, prefix=prefix, with_fake_url=False
    )
    doi = d.public_doi(example_metadata, url)
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    metadata = {"publisher": "Invenio"}
    new_metadata = d.update_doi(doi, metadata)
    assert new_metadata["publisher"] == "Invenio"
    url = "https://github.com/inveniosoftware"
    new_metadata = d.update_doi(doi, url=url)
    assert new_metadata["url"] == url


@pytest.mark.parametrize("example_json45", TEST_45_JSON_FILES)
@pytest.mark.pw
def test_rest_create_public_45(example_json45):
    """Test creating DOIs with all example metadata"""
    example_metadata = load_json_path(example_json45)
    # We need to remove the example doi, since we want DataCite to
    # mint one with our test prefix
    example_metadata.pop("doi")
    example_metadata.pop("prefix")
    example_metadata.pop("suffix")
    url = "https://github.com/inveniosoftware/datacite"
    username, password, prefix = get_credentials()
    d = get_rest(
        username=username, password=password, prefix=prefix, with_fake_url=False
    )
    doi = d.public_doi(example_metadata, url)
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    metadata = {"subjects": [{"subject": "Invenio"}]}
    new_metadata = d.update_doi(doi, metadata)
    assert new_metadata["subjects"][0]["subject"] == "Invenio"
    url = "https://github.com/inveniosoftware"
    new_metadata = d.update_doi(doi, url=url)
    assert new_metadata["url"] == url


@responses.activate
def test_rest_create_public_mock():
    """Test creating DOI"""
    prefix = "10.1234"
    example_json43 = "data/datacite-v4.3-full-example.json"
    example_metadata = load_json_path(example_json43)
    url = "https://github.com/inveniosoftware/datacite"
    data = {"data": {"id": prefix + "/1", "attributes": {"url": url}}}
    responses.add(
        responses.POST,
        "{0}dois".format(RESTURL),
        json=data,
        status=201,
    )
    d = get_rest(username="mock", password="mock", prefix=prefix)
    doi = d.public_doi(example_metadata, url)
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    url = "https://github.com/inveniosoftware"
    data = {
        "data": {
            "id": prefix + "/1",
            "attributes": {"publisher": "Invenio", "url": url},
        }
    }
    responses.add(
        responses.PUT,
        "{0}dois/{1}/1".format(RESTURL, prefix),
        json=data,
        status=200,
    )
    metadata = {"publisher": "Invenio"}
    new_metadata = d.update_doi(doi, metadata)
    assert new_metadata["publisher"] == "Invenio"
    new_metadata = d.update_doi(doi, url=url)
    assert new_metadata["url"] == url


@pytest.mark.pw
def test_rest_create_private():
    """Test creating private DOI"""
    example_json43 = "data/4.3/datacite-example-dataset-v4.json"
    example_metadata = load_json_path(example_json43)
    url = "https://github.com/inveniosoftware/datacite"
    username, password, prefix = get_credentials()
    d = get_rest(
        username=username, password=password, prefix=prefix, with_fake_url=False
    )
    doi = d.private_doi(example_metadata, url)
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    datacite_metadata = d.get_metadata(doi)
    assert datacite_metadata["state"] == "registered"
    new_metadata = d.show_doi(doi)
    assert new_metadata["state"] == "findable"
    new_metadata = d.hide_doi(doi)
    assert new_metadata["state"] == "registered"


@responses.activate
def test_rest_create_private_mock():
    """Test creating private DOI"""
    example_json43 = "data/4.3/datacite-example-dataset-v4.json"
    example_metadata = load_json_path(example_json43)
    prefix = "10.1234"
    url = "https://github.com/inveniosoftware/datacite"
    data = {
        "data": {"id": prefix + "/1", "attributes": {"state": "registered", "url": url}}
    }
    responses.add(
        responses.POST,
        "{0}dois".format(RESTURL),
        json=data,
        status=201,
    )
    responses.add(
        responses.GET,
        "{0}dois/{1}/1".format(RESTURL, prefix),
        json=data,
        status=200,
    )
    d = get_rest(username="mock", password="mock", prefix=prefix)
    doi = d.private_doi(example_metadata, url)
    datacite_prefix = doi.split("/")[0]
    assert datacite_prefix == prefix
    datacite_metadata = d.get_metadata(doi)
    assert datacite_metadata["state"] == "registered"
    data = {
        "data": {"id": prefix + "/1", "attributes": {"state": "findable", "url": url}}
    }
    responses.add(
        responses.PUT,
        "{0}dois/{1}/1".format(RESTURL, prefix),
        json=data,
        status=200,
    )
    new_metadata = d.show_doi(doi)
    assert new_metadata["state"] == "findable"


@responses.activate
def test_rest_get_200():
    """Test."""
    url = "http://example.org"
    data = {"data": {"id": "10.1234/1", "attributes": {"url": url}}}
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        json=data,
        status=200,
    )

    d = get_rest()
    assert url == d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_204():
    """Test 204 error when no content."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        status=204,
    )

    d = get_rest()
    with pytest.raises(DataCiteNoContentError):
        d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_401():
    """Test 401 error."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        body="Unauthorized",
        status=401,
    )

    d = get_rest()
    with pytest.raises(DataCiteUnauthorizedError):
        d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_403():
    """Test 403 error."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        body="Forbidden",
        status=403,
    )

    d = get_rest()
    with pytest.raises(DataCiteForbiddenError):
        d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_404():
    """Test 404 error."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        body="Not Found",
        status=404,
    )

    d = get_rest()
    with pytest.raises(DataCiteNotFoundError):
        d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_410():
    """Test 410 error."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        body="Gone",
        status=410,
    )

    d = get_rest()
    with pytest.raises(DataCiteGoneError):
        d.get_doi("10.1234/1")


@responses.activate
def test_get_doi_500():
    """Test 500 error."""
    responses.add(
        responses.GET,
        "{0}dois/10.1234/1".format(RESTURL),
        body="Internal Server Error",
        status=500,
    )

    d = get_rest()
    with pytest.raises(DataCiteServerError):
        d.get_doi("10.1234/1")
