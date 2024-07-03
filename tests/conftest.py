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

import json
from os.path import dirname, join

import pytest
import responses
from lxml import etree


def pytest_addoption(parser):
    """Add option to run tests that require password."""
    parser.addoption(
        "--runpw",
        action="store_true",
        default=False,
        help="run tests that require password",
    )


def pytest_collection_modifyitems(config, items):
    """Set up skipping for pw marked items."""
    if config.getoption("--runpw"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_pw = pytest.mark.skip(reason="need --runpw option to run")
    for item in items:
        if "pw" in item.keywords:
            item.add_marker(skip_pw)


@pytest.fixture
def example_json_file():
    """Load DataCite v3.1 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v3.1-full-example.json")) as file:
        return file.read()


@pytest.fixture
def example_json_file40():
    """Load DataCite v4.0 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v4.0-full-example.json")) as file:
        return file.read()


@pytest.fixture
def example_json_file41():
    """Load DataCite v4.1 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v4.1-full-example.json")) as file:
        return file.read()


@pytest.fixture
def example_json_file42():
    """Load DataCite v4.2 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v4.2-full-example.json")) as file:
        return file.read()


@pytest.fixture
def example_json_file43():
    """Load DataCite v4.3 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v4.3-full-example.json")) as file:
        return file.read()


@pytest.fixture
def example_json_file45():
    """Load DataCite v4.5 full example JSON."""
    path = dirname(__file__)
    with open(join(path, "data", "datacite-v4.5-full-example.json")) as file:
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
def example_json41(example_json_file41):
    """Load the DataCite v4.1 full example into a dict."""
    return json.loads(example_json_file41)


@pytest.fixture
def example_json42(example_json_file42):
    """Load the DataCite v4.2 full example into a dict."""
    return json.loads(example_json_file42)


@pytest.fixture
def example_json43(example_json_file43):
    """Load the DataCite v4.3 full example into a dict."""
    return json.loads(example_json_file43)


@pytest.fixture
def example_json45(example_json_file45):
    """Load the DataCite v4.5 full example into a dict."""
    return json.loads(example_json_file45)


def load_xml(filename):
    """Helper method for loading the XML example file."""
    path = dirname(__file__)
    with open(join(path, "data", filename)) as file:
        content = file.read()
    return content


@pytest.fixture
def example_xml_file():
    """Load DataCite v3.1 full example XML."""
    return load_xml("datacite-v3.1-full-example.xml")


@pytest.fixture
def example_xml_file40():
    """Load DataCite v4.0 full example XML."""
    return load_xml("datacite-v4.0-full-example.xml")


@pytest.fixture
def example_xml_file41():
    """Load DataCite v4.1 full example XML."""
    return load_xml("datacite-v4.1-full-example.xml")


@pytest.fixture
def example_xml_file42():
    """Load DataCite v4.2 full example XML."""
    return load_xml("datacite-v4.2-full-example.xml")


@pytest.fixture
def example_xml_file43():
    """Load DataCite v4.3 full example XML."""
    return load_xml("datacite-v4.3-full-example.xml")


@pytest.fixture
def example_xml_file45():
    """Load DataCite v4.5 full example XML."""
    return load_xml("datacite-v4.5-full-example.xml")


@pytest.fixture
def example_xml(example_xml_file):
    """Load DataCite v3.1 full example as an etree."""
    return etree.fromstring(example_xml_file.encode("utf-8"))


@pytest.fixture
def example_xml40(example_xml_file40):
    """Load DataCite v4.0 full example as an etree."""
    return etree.fromstring(example_xml_file40.encode("utf-8"))


@pytest.fixture
def example_xml41(example_xml_file41):
    """Load DataCite v4.1 full example as an etree."""
    return etree.fromstring(example_xml_file41.encode("utf-8"))


@pytest.fixture
def example_xml42(example_xml_file42):
    """Load DataCite v4.2 full example as an etree."""
    return etree.fromstring(example_xml_file42.encode("utf-8"))


@pytest.fixture
def example_xml43(example_xml_file43):
    """Load DataCite v4.3 full example as an etree."""
    return etree.fromstring(example_xml_file43.encode("utf-8"))


@pytest.fixture
def example_xml45(example_xml_file45):
    """Load DataCite v4.3 full example as an etree."""
    return etree.fromstring(example_xml_file45.encode("utf-8"))


def _load_xsd(xsd_filename):
    """Load one of the XSD schemas."""
    with open(join(dirname(__file__), "data", "xml.xsd")) as fp:
        xmlxsd = fp.read()

    # Ensure the schema validator doesn't make any http requests.
    responses.add(responses.GET, "https://www.w3.org/2009/01/xml.xsd", body=xmlxsd)

    return etree.XMLSchema(
        file="file://" + join(dirname(__file__), "data", xsd_filename)
    )


@pytest.fixture(scope="session")
def xsd31():
    """Load DataCite v3.1 full example as an etree."""
    return _load_xsd("metadata31.xsd")


@pytest.fixture(scope="session")
def xsd40():
    """Load DataCite v4.0 full example as an etree."""
    return _load_xsd("metadata40.xsd")


@pytest.fixture(scope="session")
def xsd41():
    """Load DataCite v4.1 full example as an etree."""
    return _load_xsd("metadata41.xsd")


@pytest.fixture(scope="session")
def xsd42():
    """Load DataCite v4.2 full example as an etree."""
    return _load_xsd("4.2/metadata.xsd")


@pytest.fixture(scope="session")
def xsd43():
    """Load DataCite v4.3 full example as an etree."""
    return _load_xsd("4.3/metadata.xsd")


@pytest.fixture(scope="session")
def xsd45():
    """Load DataCite v4.5 full example as an etree."""
    return _load_xsd("4.5/metadata.xsd")


@pytest.fixture(scope="function")
def minimal_json42():
    """Minimal valid JSON for DataCite 4.2."""
    return {
        "identifiers": [
            {
                "identifierType": "DOI",
                "identifier": "10.1234/foo.bar",
            }
        ],
        "creators": [
            {"name": "Nielsen, Lars Holm"},
        ],
        "titles": [{"title": "Minimal Test Case"}],
        "publisher": "Invenio Software",
        "publicationYear": "2016",
        "types": {"resourceType": "", "resourceTypeGeneral": "Software"},
        "schemaVersion": "http://datacite.org/schema/kernel-4",
    }


@pytest.fixture(scope="function")
def minimal_json43():
    """Minimal valid JSON for DataCite 4.3."""
    return {
        "identifiers": [
            {
                "identifierType": "DOI",
                "identifier": "10.1234/foo.bar",
            }
        ],
        "creators": [
            {"name": "Nielsen, Lars Holm"},
        ],
        "titles": [{"title": "Minimal Test Case"}],
        "publisher": "Invenio Software",
        "publicationYear": "2016",
        "types": {"resourceType": "", "resourceTypeGeneral": "Software"},
        "schemaVersion": "http://datacite.org/schema/kernel-4",
    }


@pytest.fixture(scope="function")
def minimal_json45():
    """Minimal valid JSON for DataCite 4.5."""
    return {
        "doi": "10.1234/foo.bar",
        "creators": [
            {"name": "Nielsen, Lars Holm"},
        ],
        "titles": [{"title": "Minimal Test Case"}],
        "publisher": {"name": "Invenio Software"},
        "publicationYear": "2016",
        "types": {"resourceType": "", "resourceTypeGeneral": "Software"},
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "url": "https://www.example.com",
    }
