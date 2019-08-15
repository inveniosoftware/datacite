# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""XML utilities."""


from collections import OrderedDict
from lxml import etree


def dump_etree_helper(data, rules, nsmap, attrib):
    """Convert DataCite JSON format to DataCite XML.

    JSON should be validated before it is given to to_xml.
    """
    output = etree.Element('resource', nsmap=nsmap, attrib=attrib)

    for rule in rules:
        if rule not in data:
            continue

        element = rules[rule](rule, data[rule])
        if element is not None:
            # Handle multiple elements coming from a rule
            if isinstance(element, tuple):
                for e in element:
                    output.append(e)
            else:
                output.append(element)

    return output


def etree_to_string(root, pretty_print=True, xml_declaration=True,
                    encoding='utf-8'):
    """Dump XML etree as a string."""
    return etree.tostring(
        root,
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        encoding=encoding,
    ).decode('utf-8')


def set_elem_attr(element, attrib, data):
    """Set a tag for an XML element if the value is not empty."""
    if attrib in data and data[attrib]:
        element.set(attrib, data[attrib])


def set_non_empty_attr(element, attribute, value):
    """Set a tag for an XML element if the value is not empty."""
    if value:
        element.set(attribute, value)


class Rules(object):
    """Rules container."""

    def __init__(self):
        """Initialize rules object."""
        self.rules = OrderedDict()

    def __getitem__(self, key):
        """Get rule for key."""
        return self.rules[key]

    def __iter__(self):
        """Get iterator for rules."""
        return iter(self.rules)

    def rule(self, key):
        """Decorate as a rule for a key in top level JSON."""
        def register(f):
            if key in self.rules:
                raise ValueError(
                    'Rule for "{0}" already registered'.format(key))
            self.rules[key] = f
            return f
        return register
