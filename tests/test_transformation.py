# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Tests for format transformations."""

from __future__ import absolute_import, unicode_literals, print_function

import pytest

from datacite.transformation import to_xml, dump_xml


def test_example_json_validates(example_json, validator):
    """Test the example file validates against the JSON schema."""
    assert validator.is_valid(example_json)


@pytest.mark.skip
def test_xml_to_json(example_xml_file):
    """Tests that example XML converts to example JSON."""
    pass


def test_json_to_xml(example_xml, example_json_file):
    """Tests that example XML converts to example JSON."""
    assert dump_xml(example_xml) == dump_xml(to_xml(example_json_file))
