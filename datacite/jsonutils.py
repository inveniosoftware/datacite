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
from jsonschema import RefResolver, validate
from jsonschema.validators import validator_for


def validator_factory(schema_filename):
    """Provide a JSON schema validator for a given schema file."""
    with open(schema_filename, 'r') as fp:
        schema = json.load(fp)

    validator_cls = validator_for(schema)
    validator_cls.check_schema(schema)

    return validator_cls(
        schema,
        resolver=RefResolver('file:{}'.format(schema_filename), schema)
    )
