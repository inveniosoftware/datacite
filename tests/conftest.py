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
def example_json(example_json_file):
    """Load the DataCite v3.1 full example into a dict."""
    return json.loads(example_json_file)


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
def example_xml(example_xml_file):
    """Load DataCite v3.1 full example as an etree."""
    return etree.fromstring(example_xml_file.encode('utf-8'))


@pytest.fixture(scope='session')
def xsd31():
    """Load DataCite v3.1 full example as an etree."""
    return etree.XMLSchema(
        file='file://' + join(dirname(__file__), 'data', 'metadata31.xsd')
    )
