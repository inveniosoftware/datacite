# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test helpers."""

import io
import json
import os
from os.path import dirname, join

from datacite import DataCiteMDSClient, DataCiteRESTClient

APIURL = "https://mds.example.org/"
RESTURL = "https://doi.example.org/"


def get_client(username="DC", password="pw", prefix="10.1234", with_fake_url=True):
    """Create a API client."""
    client = DataCiteMDSClient(
        username=username,
        password=password,
        prefix=prefix,
        test_mode=True,
    )
    if with_fake_url:
        # change URL for tests
        client.api_url = APIURL
    return client


def get_rest(username="DC", password="pw", prefix="10.1234", with_fake_url=True):
    """Create a REST API client."""
    client = DataCiteRESTClient(
        username=username,
        password=password,
        prefix=prefix,
        test_mode=True,
    )
    if with_fake_url:
        # change URL for tests
        client.api_url = RESTURL
    return client


def get_credentials():
    """Helper method for getting credentials from environment."""
    username = os.environ["DATACITE_USER"]
    password = os.environ["DATACITE_PW"]
    prefix = os.environ["DATACITE_PREFIX"]
    return username, password, prefix


def load_xml_path(path):
    """Helper method for loading an XML example file from a path."""
    path_base = dirname(__file__)
    with io.open(join(path_base, path), encoding="utf-8") as file:
        content = file.read()
    return content


def load_json_path(path):
    """Helper method for loading a JSON example file from a path."""
    path_base = dirname(__file__)
    with io.open(join(path_base, path), encoding="utf-8") as file:
        content = file.read()
    return json.loads(content)


#
# Tests on example files
#
TEST_43_JSON_FILES = [
    "data/4.3/datacite-example-polygon-v4.json",
    "data/4.3/datacite-example-fundingReference-v4.json",
    "data/4.3/datacite-example-ResearchGroup_Methods-v4.json",
    "data/4.3/datacite-example-complicated-v4.json",
    "data/4.3/datacite-example-datapaper-v4.json",
    "data/4.3/datacite-example-video-v4.json",
    "data/4.3/datacite-example-dataset-v4.json",
    "data/4.3/datacite-example-Box_dateCollected_DataCollector-v4.json",
    "data/4.3/datacite-example-ResourceTypeGeneral_Collection-v4.json",
    "data/4.3/datacite-example-HasMetadata-v4.json",
    "data/4.3/datacite-example-workflow-v4.json",
    "data/4.3/datacite-example-GeoLocation-v4.json",
    "data/4.3/datacite-example-relationTypeIsIdenticalTo-v4.json",
    "data/4.3/datacite-example-software-v4.json",
    "data/4.3/datacite-example-affiliation-v4.json",
    "data/4.3/datacite-example-ancientdates-v4.json",
    "data/datacite-v4.3-full-example.json",
]

TEST_45_JSON_FILES = [
    "data/4.5/datacite-example-dataset-v4.json",
    "data/4.5/datacite-example-instrument-v4.json",
    "data/4.5/datacite-example-multilingual-v4.json",
    "data/4.5/datacite-example-relateditem1-v4.json",
    "data/4.5/datacite-example-relateditem2-v4.json",
    "data/4.5/datacite-example-relateditem3-v4.json",
    "data/datacite-v4.5-full-example.json",
]
