# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import json
from os.path import dirname, join

import httpretty
import pytest
from lxml import etree


@pytest.fixture
def example_json_file():
    """Load DataCite v3.1 full example JSON."""
    path = dirname(__file__)
    with open(join(
            path,
            'data',
            'datacite-v3.1-full-example.json')) as file:
        return file.read()


@pytest.fixture
def example_json_file40():
    """Load DataCite v4.0 full example JSON."""
    path = dirname(__file__)
    with open(join(
            path,
            'data',
            'datacite-v4.0-full-example.json')) as file:
        return file.read()


@pytest.fixture
def example_json(example_json_file):
    """Load the DataCite v3.1 full example into a dict."""
    return json.loads(example_json_file)


@pytest.fixture
def example_json40(example_json_file40):
    """Load the DataCite v4.0 full example into a dict."""
    return json.loads(example_json_file40)


@pytest.fixture
def example_xml_file():
    """Load DataCite v3.1 full example XML."""
    path = dirname(__file__)
    with open(join(
            path,
            'data',
            'datacite-v3.1-full-example.xml')) as file:
        return file.read()


@pytest.fixture
def example_xml_file40():
    """Load DataCite v4.0 full example XML."""
    path = dirname(__file__)
    with open(join(
            path,
            'data',
            'datacite-v4.0-full-example.xml')) as file:
        return file.read()


@pytest.fixture
def example_xml(example_xml_file):
    """Load DataCite v3.1 full example as an etree."""
    return etree.fromstring(example_xml_file.encode('utf-8'))


@pytest.fixture
def example_xml40(example_xml_file40):
    """Load DataCite v4.0 full example as an etree."""
    return etree.fromstring(example_xml_file40.encode('utf-8'))


@pytest.yield_fixture(scope='session')
def xsd31():
    """Load DataCite v3.1 full example as an etree."""
    # Ensure the schema validator doesn't make any http requests.
    with open(join(dirname(__file__), 'data', 'xml.xsd')) as fp:
        xmlxsd = fp.read()

    httpretty.enable()
    httpretty.register_uri(
        httpretty.GET,
        'https://www.w3.org/2009/01/xml.xsd',
        body=xmlxsd)

    yield etree.XMLSchema(
        file='file://' + join(dirname(__file__), 'data', 'metadata31.xsd')
    )

    httpretty.disable()


@pytest.yield_fixture(scope='session')
def xsd40():
    """Load DataCite v4.0 full example as an etree."""
    # Ensure the schema validator doesn't make any http requests.
    with open(join(dirname(__file__), 'data', 'xml.xsd')) as fp:
        xmlxsd = fp.read()

    httpretty.enable()
    httpretty.register_uri(
        httpretty.GET,
        'https://www.w3.org/2009/01/xml.xsd',
        body=xmlxsd)

    yield etree.XMLSchema(
        file='file://' + join(dirname(__file__), 'data', 'metadata40.xsd')
    )

    httpretty.disable()
