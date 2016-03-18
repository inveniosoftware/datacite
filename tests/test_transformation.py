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

from __future__ import absolute_import, print_function, unicode_literals

from datacite.transformation import dump_xml, to_xml


def test_example_json_validates(example_json, validator):
    """Test the example file validates against the JSON schema."""
    assert validator.is_valid(example_json)


def test_json_to_xml(example_xml, example_json_file):
    """Test that example XML converts to example JSON."""
    assert dump_xml(example_xml) == dump_xml(to_xml(example_json_file))
