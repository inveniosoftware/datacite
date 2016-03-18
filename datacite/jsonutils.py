# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""JSON utilities."""

import json
from os.path import abspath, basename, dirname, split

import jsonschema


def validator_factory(schema_filename):
    """Provide a JSON schema validator for a given schema file."""
    schema_dir = dirname(abspath(schema_filename))
    schema_name = basename(schema_filename)

    with open(schema_filename) as fp:
        schema_json = json.load(fp)

    resolver = jsonschema.RefResolver(
        'file://'+'/'.join(split(schema_dir)) + '/', schema_name
    )

    return jsonschema.Draft4Validator(schema_json, resolver=resolver)
