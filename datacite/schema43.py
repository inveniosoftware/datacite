# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
# Copyright (C) 2019 Caltech.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""DataCite v4.3 JSON to XML transformations."""

import pkg_resources
from lxml import etree
from lxml.builder import E

from .jsonutils import validator_factory
from .xmlutils import Rules, dump_etree_helper, etree_to_string, \
    set_elem_attr, set_non_empty_attr

rules = Rules()

ns = {
    None: 'http://datacite.org/schema/kernel-4',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xml': 'xml',
}

root_attribs = {
    '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
    'http://datacite.org/schema/kernel-4 '
    'http://schema.datacite.org/meta/kernel-4.3/metadata.xsd',
}

validator = validator_factory(pkg_resources.resource_filename(
    'datacite',
    'schemas/datacite-v4.3.json'
))


def dump_etree(data):
    """Convert JSON dictionary to DataCite v4.3 XML as ElementTree."""
    return dump_etree_helper(data, rules, ns, root_attribs)


def tostring(data, **kwargs):
    """Convert JSON dictionary to DataCite v4.3 XML as string."""
    return etree_to_string(dump_etree(data), **kwargs)


def validate(data):
    """Validate DataCite v4.3 JSON dictionary."""
    return validator.is_valid(data)


@rules.rule('identifiers')
def identifiers(path, values):
    """Transform identifiers to alternateIdentifiers and identifier.

    We assume there will only be 1 DOI identifier for the record.
    Any other identifiers are alternative identifiers.
    """
    alt = ''
    doi = ''
    for value in values:
        if value['identifierType'] == 'DOI':
            if doi != '':
                # Don't know what to do with two DOIs
                # Which is the actual identifier?
                raise TypeError
            doi = E.identifier(
                value['identifier'],
                identifierType='DOI'
            )
        else:
            if alt == '':
                alt = E.alternateIdentifiers()
            elem = E.alternateIdentifier(value['identifier'])
            elem.set('alternateIdentifierType', value['identifierType'])
            alt.append(elem)
    if alt == '':
        # If we only have the DOI
        return doi
    elif doi == '':
        # If we only have alt IDs
        return alt
    else:
        return doi, alt


def affiliation(root, values):
    """Extract affiliation."""
    vals = values.get('affiliation', [])
    for val in vals:
        if val.get('name'):
            elem = E.affiliation(val['name'])
            # affiliationIdentifier metadata as Attributes
            # (0-1 cardinality, instead of 0-n as list of objects)
            set_elem_attr(elem, 'affiliationIdentifier', val)
            set_elem_attr(elem, 'affiliationIdentifierScheme', val)
            if val.get('schemeUri'):
                elem.set('schemeURI', val['schemeUri'])
            root.append(elem)


def familyname(root, value):
    """Extract family name."""
    val = value.get('familyName')
    if val:
        root.append(E.familyName(val))


def givenname(root, value):
    """Extract family name."""
    val = value.get('givenName')
    if val:
        root.append(E.givenName(val))


def person_or_org_name(root, value, xml_tagname, json_tagname):
    """Extract creator/contributor name and it's 'nameType' attribute."""
    elem = E(xml_tagname, value[json_tagname])
    set_elem_attr(elem, 'nameType', value)
    set_non_empty_attr(elem, '{xml}lang', value.get('lang'))
    root.append(elem)


def nameidentifiers(root, values):
    """Extract nameidentifier."""
    vals = values.get('nameIdentifiers', [])
    for val in vals:
        if val.get('nameIdentifier'):
            elem = E.nameIdentifier(val['nameIdentifier'])
            elem.set('nameIdentifierScheme', val['nameIdentifierScheme'])
            if val.get('schemeUri'):
                elem.set('schemeURI', val['schemeUri'])
            root.append(elem)


@rules.rule('creators')
def creators(path, values):
    """Transform creators."""
    if not values:
        return

    root = E.creators()
    for value in values:
        creator = E.creator()
        person_or_org_name(creator, value, 'creatorName', 'name')
        givenname(creator, value)
        familyname(creator, value)
        nameidentifiers(creator, value)
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
        # 'type' was a mistake in 4.0 serializer, which is supported
        # for backwards compatibility until kernel 5 is released.
        set_non_empty_attr(elem, 'titleType', value.get('type'))
        # 'titleType' will supersede 'type' if available
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
        set_elem_attr(elem, 'subjectScheme', value)
        if value.get('schemeUri'):
            elem.set('schemeURI', value['schemeUri'])
        if value.get('valueUri'):
            elem.set('valueURI', value['valueUri'])
        root.append(elem)
    return root


@rules.rule('contributors')
def contributors(path, values):
    """Transform contributors."""
    if not values:
        return

    root = E.contributors()
    for value in values:
        contributor = E.contributor()
        person_or_org_name(contributor, value, 'contributorName', 'name')
        set_elem_attr(contributor, 'contributorType', value)
        givenname(contributor, value)
        familyname(contributor, value)
        nameidentifiers(contributor, value)
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
        elem = E.date(value['date'], dateType=value['dateType'])
        set_elem_attr(elem, 'dateInformation', value)
        root.append(elem)

    return root


@rules.rule('language')
def language(path, value):
    """Transform language."""
    if not value:
        return
    return E.language(value)


@rules.rule('types')
def resource_type(path, value):
    """Transform resourceType."""
    elem = E.resourceType()
    elem.set('resourceTypeGeneral', value['resourceTypeGeneral'])
    elem.text = value['resourceType']
    return elem


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
        if value.get('schemeUri'):
            elem.set('schemeURI', value['schemeUri'])
        set_elem_attr(elem, 'schemeType', value)
        set_elem_attr(elem, 'resourceTypeGeneral', value)
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
        if 'rights' in value:
            elem = E.rights(value['rights'])
        # Handle the odd case where no rights text present
        else:
            elem = E.rights()
        if value.get('rightsUri'):
            elem.set('rightsURI', value['rightsUri'])
        set_elem_attr(elem, 'rightsIdentifierScheme', value)
        set_elem_attr(elem, 'rightsIdentifier', value)
        if value.get('schemeUri'):
            elem.set('schemeURI', value['schemeUri'])
        set_non_empty_attr(elem, '{xml}lang', value.get('lang'))
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
        set_non_empty_attr(elem, '{xml}lang', value.get('lang'))
        root.append(elem)

    return root


def geopoint(root, value):
    """Extract a point (either geoLocationPoint or polygonPoint)."""
    root.append(E.pointLongitude(str(value['pointLongitude'])))
    root.append(E.pointLatitude(str(value['pointLatitude'])))


@rules.rule('geoLocations')
def geolocations(path, values):
    """Transform geolocations."""
    if not values:
        return

    root = E.geoLocations()
    for value in values:
        element = E.geoLocation()

        place = value.get('geoLocationPlace')
        if place:
            element.append(E.geoLocationPlace(place))

        point = value.get('geoLocationPoint')
        if point:
            elem = E.geoLocationPoint()
            geopoint(elem, point)
            element.append(elem)

        box = value.get('geoLocationBox')
        if box:
            elem = E.geoLocationBox()
            elem.append(E.westBoundLongitude(str(box['westBoundLongitude'])))
            elem.append(E.eastBoundLongitude(str(box['eastBoundLongitude'])))
            elem.append(E.southBoundLatitude(str(box['southBoundLatitude'])))
            elem.append(E.northBoundLatitude(str(box['northBoundLatitude'])))
            element.append(elem)

        polygons = value.get('geoLocationPolygons', [])
        for polygon in polygons:
            elem = E.geoLocationPolygon()
            points = polygon["polygonPoints"]
            for p in points:
                e = E.polygonPoint()
                geopoint(e, p)
                elem.append(e)
            inPoint = polygon.get("inPolygonPoint")
            if inPoint:
                e = E.inPolygonPoint()
                geopoint(e, inPoint)
                elem.append(e)
            element.append(elem)

        root.append(element)
    return root


@rules.rule('fundingReferences')
def fundingreferences(path, values):
    """Transform funding references."""
    if not values:
        return

    root = E.fundingReferences()
    for value in values:
        element = E.fundingReference()

        element.append(E.funderName(value.get('funderName')))

        identifier = value.get('funderIdentifier')
        if identifier:
            elem = E.funderIdentifier(identifier)
            typev = value.get('funderIdentifierType')
            if typev:
                elem.set('funderIdentifierType', typev)
            element.append(elem)

        number = value.get('awardNumber')
        if number:
            elem = E.awardNumber(number)
            uri = value.get('awardUri')
            if uri:
                elem.set('awardURI', uri)
            element.append(elem)

        title = value.get('awardTitle')
        if title:
            element.append(E.awardTitle(title))
        if len(element):
            root.append(element)
    return root
