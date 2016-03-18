# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""DataCite JSON to XML transformations."""

from __future__ import absolute_import, print_function

import json
from collections import OrderedDict

from lxml import etree

rules = OrderedDict()

# ns = OrderedDict()
# ns[None] = 'http://datacite.org/schema/kernel-3',
# ns['xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'

ns = {
    None: 'http://datacite.org/schema/kernel-3',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xml': 'xml',
}


def to_xml(record_json):
    """Convert DataCite JSON format to DataCite XML.

    JSON should be validated before it is given to to_xml.
    """
    record = json.loads(record_json)
    output = etree.Element('resource', nsmap=ns, attrib={
            '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
            'http://datacite.org/schema/kernel-3 '
            'http://schema.datacite.org/meta/kernel-3/metadata.xsd',
        }
    )

    for rule in rules:
        if rule not in record:
            continue

        output.append(rules[rule](rule, record[rule]))

    return output


def dump_xml(root):
    """Dump XML etree as a string."""
    return etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8',
    ).decode('utf-8')


def set_non_empty_attr(element, attribute, value):
    """Set a tag for an XML element if the value is not empty."""
    if value:
        element.set(attribute, value)


def rule(key):
    """Decorate as a rule for a key in top level JSON."""
    def register(f):
        if key in rules:
            raise ValueError('rule for "{0}" already registerd'.format(key))
        rules[key] = f
        return f
    return register


@rule('identifier')
def identifier(path, value):
    """Transform identifier."""
    element = etree.Element('identifier')
    element.text = value.get('identifier')
    element.set('identifierType', value.get('type'))
    return element


@rule('creators')
def creators(path, values):
    """Transform creators."""
    root = etree.Element('creators')
    for value in values:
        creatorElem = etree.SubElement(root, 'creator')
        etree.SubElement(creatorElem, 'creatorName').text = value.get('name')

        nameIdElem = etree.SubElement(creatorElem, 'nameIdentifier')
        identifier = value.get('identifier', {})
        scheme = identifier.get('scheme', {})
        nameIdElem.text = identifier.get('identifier')
        set_non_empty_attr(nameIdElem, 'schemeURI', scheme.get('uri'))
        set_non_empty_attr(
            nameIdElem, 'nameIdentifierScheme', scheme.get('name'))

        affliationElem = etree.SubElement(creatorElem, 'affiliation')
        affliationElem.text = value.get('affiliation')
    return root


@rule('titles')
def titles(path, values):
    """Transform titles."""
    root = etree.Element('titles')
    for value in values:
        titleElem = etree.SubElement(root, 'title', nsmap=ns)
        titleElem.text = value.get('title')
        set_non_empty_attr(titleElem, '{xml}lang', value.get('language'))
        set_non_empty_attr(titleElem, 'titleType', value.get('type'))
    return root


@rule('publisher')
def publisher(path, value):
    """Transform publisher."""
    elem = etree.Element('publisher')
    elem.text = value
    return elem


@rule('publicationYear')
def publication_year(path, value):
    """Transform publicationYear."""
    elem = etree.Element('publicationYear')
    elem.text = str(value)
    return elem


@rule('subjects')
def subjects(path, values):
    """Transform subjects."""
    root = etree.Element('subjects')
    for value in values:
        subjectElem = etree.SubElement(root, 'subject')
        subjectElem.text = value.get('subject')
        set_non_empty_attr(subjectElem, '{xml}lang', value.get('language'))

        scheme = value.get('scheme', {})
        set_non_empty_attr(subjectElem, 'schemeURI', scheme.get('uri'))
        set_non_empty_attr(subjectElem, 'subjectScheme', scheme.get('name'))
    return root


@rule('contributors')
def contributors(path, values):
    """Transform contributors."""
    root = etree.Element('contributors')
    for value in values:
        contributorElem = etree.SubElement(root, 'contributor')
        set_non_empty_attr(
            contributorElem, 'contributorType', value.get('type')
        )

        nameElem = etree.SubElement(contributorElem, 'contributorName')
        nameElem.text = value.get('name')

        identifier = value.get('identifier', {})
        scheme = identifier.get('scheme', {})
        nameIdentifierElem = etree.SubElement(contributorElem,
                                              'nameIdentifier')
        nameIdentifierElem.text = identifier.get('identifier')
        set_non_empty_attr(nameIdentifierElem, 'schemeURI', scheme.get('uri'))
        set_non_empty_attr(
            nameIdentifierElem, 'nameIdentifierScheme', scheme.get('name')
        )

        affliationElem = etree.SubElement(contributorElem, 'affiliation')
        affliationElem.text = value.get('affiliation')
    return root


@rule('dates')
def dates(path, values):
    """Transform dates."""
    root = etree.Element('dates')
    for value in values:
        dateElem = etree.SubElement(root, 'date')
        dateElem.text = value.get('date')
        set_non_empty_attr(dateElem, 'dateType', value.get('type'))
    return root


@rule('language')
def language(path, value):
    """Transform language."""
    elem = etree.Element('language')
    elem.text = value
    return elem


@rule('resourceType')
def resource_type(path, value):
    """Transform resourceType."""
    elem = etree.Element('resourceType')
    elem.text = value.get('type')
    set_non_empty_attr(elem, 'resourceTypeGeneral', value.get('general'))
    return elem


@rule('alternateIdentifiers')
def alternate_identifiers(path, values):
    """Transform alternateIdenftifiers."""
    root = etree.Element('alternateIdentifiers')
    for value in values:
        idElem = etree.SubElement(root, 'alternateIdentifier')
        idElem.text = value.get('identifier')
        set_non_empty_attr(
            idElem, 'alternateIdentifierType', value.get('type')
        )
    return root


@rule('relatedIdentifiers')
def related_identifiers(path, values):
    """Transform relatedIdentifiers."""
    root = etree.Element('relatedIdentifiers')
    for value in values:
        idElem = etree.SubElement(root, 'relatedIdentifier')
        idElem.text = value.get('identifier')
        set_non_empty_attr(idElem, 'relatedIdentifierType', value.get('type'))
        set_non_empty_attr(idElem, 'relationType', value.get('relation'))

        scheme = value.get('scheme', {})
        set_non_empty_attr(idElem, 'relatedMetadataScheme', scheme.get('name'))
        set_non_empty_attr(idElem, 'schemeURI', scheme.get('uri'))
    return root


@rule('sizes')
def sizes(path, values):
    """Transform sizes."""
    root = etree.Element('sizes')
    for value in values:
        etree.SubElement(root, 'size').text = value
    return root


@rule('formats')
def formats(path, values):
    """Transform formats."""
    root = etree.Element('formats')
    for value in values:
        etree.SubElement(root, 'format').text = value
    return root


@rule('version')
def version(path, value):
    """Transform version."""
    element = etree.Element('version')
    element.text = value
    return element


@rule('rights')
def rights(path, values):
    """Transform rights."""
    root = etree.Element('rightsList')
    for value in values:
        elem = etree.SubElement(root, 'rights')
        elem.text = value.get('name')
        set_non_empty_attr(elem, 'rightsURI', value.get('uri'))
    return root


@rule('descriptions')
def descriptions(path, values):
    """Transform descriptions."""
    root = etree.Element('descriptions')
    for value in values:
        elem = etree.SubElement(root, 'description')
        elem.text = value.get('description')
        set_non_empty_attr(elem, '{xml}lang', value.get('language'))
        set_non_empty_attr(elem, 'descriptionType', value.get('type'))
    return root


@rule('geolocations')
def geolocations(path, values):
    """Transform geolocations."""
    root = etree.Element('geoLocations')
    for value in values:
        locElem = etree.SubElement(root, 'geoLocation')

        point = value.get('point')
        if point:
            pointElem = etree.SubElement(locElem, 'geoLocationPoint')
            pointElem.text = '{0:.3f} {1:.3f}'.format(
                point['latitude'], point['longitude']
            )

        box = value.get('box')
        if box:
            boxElem = etree.SubElement(locElem, 'geoLocationBox')
            boxElem.text = '{0:.3f} {1:.3f}  {2:.3f} {3:.3f}'.format(
                box['latitude1'],
                box['longitude1'],
                box['latitude2'],
                box['longitude2']
            )

        place = value.get('place')
        if place:
            placeElem = etree.SubElement(locElem, 'geoLocationPlace')
            placeElem.text = place
    return root
