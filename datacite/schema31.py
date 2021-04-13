# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""DataCite v3.1 JSON to XML transformations."""

import pkg_resources
from lxml import etree
from lxml.builder import E

from .jsonutils import validator_factory
from .xmlutils import Rules, dump_etree_helper, etree_to_string, \
    set_elem_attr, set_non_empty_attr

rules = Rules()

ns = {
    None: 'http://datacite.org/schema/kernel-3',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xml': 'xml',
}

root_attribs = {
    '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
    'http://datacite.org/schema/kernel-3 '
    'http://schema.datacite.org/meta/kernel-3/metadata.xsd',
}

validator = validator_factory(pkg_resources.resource_filename(
    'datacite',
    'schemas/datacite-v3.1.json'
))


def dump_etree(data):
    """Convert JSON dictionary to DataCite v3.1 XML as ElementTree."""
    return dump_etree_helper(data, rules, ns, root_attribs)


def tostring(data, **kwargs):
    """Convert JSON dictionary to DataCite v3.1 XML as string."""
    return etree_to_string(dump_etree(data), **kwargs)


def validate(data):
    """Validate DataCite v3.1 JSON dictionary."""
    return validator.is_valid(data)


@rules.rule('identifier')
def identifier(path, value):
    """Transform identifier."""
    return E.identifier(
        value['identifier'],
        identifierType=value['identifierType']
    )


def affiliation(root, value):
    """Extract affiliation."""
    val = value.get('affiliation')
    if val:
        root.append(E.affiliation(val))


def nameidentifier(root, value):
    """Extract nameidentifier."""
    val = value.get('nameIdentifier', {})
    if val.get('nameIdentifier'):
        elem = E.nameIdentifier(value['nameIdentifier']['nameIdentifier'])
        elem.set('nameIdentifierScheme', val['nameIdentifierScheme'])
        set_elem_attr(elem, 'schemeURI', val)
        root.append(elem)


@rules.rule('creators')
def creators(path, values):
    """Transform creators."""
    if not values:
        return

    root = E.creators()
    for value in values:
        creator = E.creator(
            E.creatorName(value['creatorName'])
        )

        nameidentifier(creator, value)
        affiliation(creator, value)
        root.append(creator)

    return root


@rules.rule('titles')
def titles(path, values):
    """Transform titles."""
    if not values:
        return
    root = E.titles()

    for value in values:
        elem = etree.Element('title', nsmap=ns)
        elem.text = value['title']
        set_non_empty_attr(elem, '{xml}lang', value.get('lang'))
        set_non_empty_attr(elem, 'titleType', value.get('titleType'))
        root.append(elem)

    return root


@rules.rule('publisher')
def publisher(path, value):
    """Transform publisher."""
    if not value:
        return
    return E.publisher(value)


@rules.rule('publicationYear')
def publication_year(path, value):
    """Transform publicationYear."""
    if not value:
        return
    return E.publicationYear(str(value))


@rules.rule('subjects')
def subjects(path, values):
    """Transform subjects."""
    if not values:
        return

    root = E.subjects()
    for value in values:
        elem = E.subject(value['subject'])
        set_non_empty_attr(elem, '{xml}lang', value.get('lang'))
        set_elem_attr(elem, 'schemeURI', value)
        set_elem_attr(elem, 'subjectScheme', value)
        root.append(elem)
    return root


@rules.rule('contributors')
def contributors(path, values):
    """Transform contributors."""
    if not values:
        return

    root = E.contributors()
    for value in values:
        contributor = E.contributor(
            E.contributorName(value['contributorName']),
            contributorType=value['contributorType']
        )
        nameidentifier(contributor, value)
        affiliation(contributor, value)
        root.append(contributor)

    return root


@rules.rule('dates')
def dates(path, values):
    """Transform dates."""
    if not values:
        return

    root = E.dates()
    for value in values:
        root.append(E.date(value['date'], dateType=value['dateType']))

    return root


@rules.rule('language')
def language(path, value):
    """Transform language."""
    if not value:
        return
    return E.language(value)


@rules.rule('resourceType')
def resource_type(path, value):
    """Transform resourceType."""
    if not value:
        return
    elem = E.resourceType()
    elem.set('resourceTypeGeneral', value['resourceTypeGeneral'])
    if value.get('resourceType'):
        elem.text = value['resourceType']
    return elem


@rules.rule('alternateIdentifiers')
def alternate_identifiers(path, values):
    """Transform alternateIdenftifiers."""
    if not values:
        return

    root = E.alternateIdentifiers()
    for value in values:
        elem = E.alternateIdentifier(value['alternateIdentifier'])
        elem.set('alternateIdentifierType', value['alternateIdentifierType'])
        root.append(elem)

    return root


@rules.rule('relatedIdentifiers')
def related_identifiers(path, values):
    """Transform relatedIdentifiers."""
    if not values:
        return

    root = E.relatedIdentifiers()
    for value in values:
        elem = E.relatedIdentifier()
        elem.text = value['relatedIdentifier']
        elem.set('relatedIdentifierType', value['relatedIdentifierType'])
        elem.set('relationType', value['relationType'])
        set_elem_attr(elem, 'relatedMetadataScheme', value)
        set_elem_attr(elem, 'schemeURI', value)
        set_elem_attr(elem, 'schemeType', value)
        root.append(elem)
    return root


def free_text_list(plural, singular, values):
    """List of elements with free text."""
    if not values:
        return
    root = etree.Element(plural)
    for value in values:
        etree.SubElement(root, singular).text = value
    return root


@rules.rule('sizes')
def sizes(path, values):
    """Transform sizes."""
    return free_text_list('sizes', 'size', values)


@rules.rule('formats')
def formats(path, values):
    """Transform sizes."""
    return free_text_list('formats', 'format', values)


@rules.rule('version')
def version(path, value):
    """Transform version."""
    if not value:
        return
    return E.version(value)


@rules.rule('rightsList')
def rights(path, values):
    """Transform rights."""
    if not values:
        return

    root = E.rightsList()
    for value in values:
        elem = E.rights(value['rights'])
        set_elem_attr(elem, 'rightsURI', value)
        root.append(elem)

    return root


@rules.rule('descriptions')
def descriptions(path, values):
    """Transform descriptions."""
    if not values:
        return

    root = E.descriptions()
    for value in values:
        elem = E.description(
            value['description'], descriptionType=value['descriptionType']
        )
        set_non_empty_attr(elem, '{xml}lang', value.get('language'))
        root.append(elem)

    return root


@rules.rule('geoLocations')
def geolocations(path, values):
    """Transform geolocations."""
    if not values:
        return

    root = E.geoLocations()
    for value in values:
        elem = E.geoLocation()

        point = value.get('geoLocationPoint')
        if point:
            elem.append(E.geoLocationPoint(point))

        box = value.get('geoLocationBox')
        if box:
            elem.append(E.geoLocationBox(box))

        place = value.get('geoLocationPlace')
        if place:
            elem.append(E.geoLocationPlace(place))

        root.append(elem)
    return root
