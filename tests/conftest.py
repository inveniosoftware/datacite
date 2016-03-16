# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

from __future__ import absolute_import, print_function

import json
import jsonschema
import os
import pkg_resources
import pytest

from lxml import etree


@pytest.fixture
def validator():
    """Provides a JSON schema validator for DataCite v3.1 schema."""
    schema = pkg_resources.resource_filename(
        'datacite',
        'schema/datacite-v3.1.jsonschema'
    )

    schema_dir = os.path.dirname(os.path.abspath(schema))
    schema_name = os.path.basename(schema)

    with open(schema) as file:
        schema_json = json.load(file)

    resolver = jsonschema.RefResolver(
        'file://'+'/'.join(os.path.split(schema_dir)) + '/', schema_name
    )

    return jsonschema.Draft4Validator(schema_json, resolver=resolver)


@pytest.fixture
def example_json_file():
    """Loads DataCite v3.1 full example JSON."""
    path = os.path.dirname(__file__)
    with open(os.path.join(
            path,
            'data',
            'datacite-v3.1-full-example.json')) as file:
        return file.read()


@pytest.fixture
def example_json(example_json_file):
    """Loads the DataCite v3.1 full example into a dict."""
    return json.loads(example_json_file)


@pytest.fixture
def example_xml_file():
    """Loads DataCite v3.1 full example XML."""
    path = os.path.dirname(__file__)
    with open(os.path.join(
            path,
            'data',
            'datacite-v3.1-full-example.xml')) as file:
        return file.read()


@pytest.fixture
def example_xml(example_xml_file):
    """Loads DataCite v3.1 full example as an etree."""
    return etree.fromstring(example_xml_file.encode('utf-8'))
