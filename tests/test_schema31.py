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

import xml.etree.ElementTree as ET

import pytest
from lxml import etree

from datacite.schema31 import dump_etree, tostring, validate
from datacite.xmlutils import Rules


def test_rules():
    """Test rules."""
    rules = Rules()

    rules.rule('a')(lambda x: 'a')
    pytest.raises(ValueError, rules.rule('a'), lambda x: 'b')


def test_example_json_validates(example_json):
    """Test the example file validates against the JSON schema."""
    assert validate(example_json)


def test_json_to_xml(example_xml_file, example_json, xsd31):
    """Test that example XML converts to example JSON."""
    xsd31.assertValid(etree.XML(example_xml_file.encode('utf8')))
    xsd31.assertValid(etree.XML(tostring(example_json).encode('utf8')))


def test_identifier():
    """Test that example XML converts to example JSON."""
    tree = dump_etree({
        'identifier': {
            'identifierType': 'DOI',
            'identifier': '10.1234/foo.bar',
        }
    })
    elem = tree.xpath('/resource/identifier')[0]
    assert elem.text == '10.1234/foo.bar'
    assert elem.get('identifierType') == 'DOI'


def test_creators():
    """Test creators."""
    pytest.raises(TypeError, dump_etree, {'creators': {'invalid': 'data'}})

    tree = dump_etree({'creators': []})
    assert len(tree.xpath('/resource/creators')) == 0

    tree = dump_etree({'creators': [{
        'creatorName': 'Smith, John'
    }]})
    assert len(tree.xpath('/resource/creators/creator')) == 1
    assert len(tree.xpath('/resource/creators/creator/creatorName')) == 1
    assert len(tree.xpath('/resource/creators/creator/nameIdentifier')) == 0
    assert len(tree.xpath('/resource/creators/creator/affiliation')) == 0

    tree = dump_etree({'creators': [{
        'creatorName': 'Smith, John',
        'affiliation': 'CERN',
        'nameIdentifier': {
            'nameIdentifier': '1234',
            'schemeURI': 'http://orcid.org',
            'nameIdentifierScheme': 'orcid',
        },
    }]})
    assert len(tree.xpath('/resource/creators/creator/creatorName')) == 1
    assert len(tree.xpath('/resource/creators/creator/nameIdentifier')) == 1
    assert len(tree.xpath('/resource/creators/creator/affiliation')) == 1


def test_titles():
    """Test titles."""
    pytest.raises(TypeError, dump_etree, {'titles': {'invalid': 'data'}})

    tree = dump_etree({'titles': []})
    assert len(tree.xpath('/resource/titles')) == 0

    tree = dump_etree({'titles': [
        {'title': 'Test'}
    ]})
    assert len(tree.xpath('/resource/titles')) == 1
    assert len(tree.xpath('/resource/titles/title')) == 1

    elem = dump_etree({'titles': [
        {'title': 'Test', 'titleType': 'Subtitle'}
    ]}).xpath('/resource/titles/title')[0]
    assert elem.text == 'Test'
    assert elem.get('titleType') == 'Subtitle'

    elem = dump_etree({'titles': [
        {'title': 'Test', 'lang': 'en'}
    ]}).xpath('/resource/titles/title')[0]
    assert elem.get('{xml}lang') == 'en'


def test_publisher():
    """Test publisher."""
    tree = dump_etree({'publisher': 'test'})
    assert tree.xpath('/resource/publisher')[0].text == 'test'

    tree = dump_etree({'publisher': ''})
    assert len(tree.xpath('/resource/publisher')) == 0


def test_publicationyear():
    """Test publisher."""
    tree = dump_etree({'publicationYear': 2002})
    assert tree.xpath('/resource/publicationYear')[0].text == '2002'

    tree = dump_etree({'publicationYear': None})
    assert len(tree.xpath('/resource/publicationYear')) == 0


def test_subjects():
    """Test creators."""
    pytest.raises(TypeError, dump_etree, {'subjects': {'invalid': 'data'}})

    tree = dump_etree({'subjects': []})
    assert len(tree.xpath('/resource/subjects')) == 0

    tree = dump_etree({'subjects': [{
        'subject': 'test'
    }]})
    assert len(tree.xpath('/resource/subjects/subject')) == 1

    elem = dump_etree({'subjects': [{
        'subject': 'test',
        'subjectScheme': 'dewey',
        'schemeURI': 'dewey-uri',
    }]}).xpath('/resource/subjects/subject')[0]
    assert elem.get('subjectScheme') == 'dewey'
    assert elem.get('schemeURI') == 'dewey-uri'


def test_contributors():
    """Test creators."""
    pytest.raises(TypeError, dump_etree, {'contributors': {'invalid': 'data'}})

    tree = dump_etree({'contributors': []})
    assert len(tree.xpath('/resource/contributors')) == 0

    tree = dump_etree({'contributors': [{
        'contributorName': 'Smith, John',
        'contributorType': 'Funder',
    }]})
    assert len(tree.xpath(
        '/resource/contributors/contributor')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/contributorName')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/nameIdentifier')) == 0
    assert len(tree.xpath(
        '/resource/contributors/contributor/affiliation')) == 0

    tree = dump_etree({'contributors': [{
        'contributorName': 'Smith, John',
        'contributorType': 'Funder',
        'affiliation': 'CERN',
        'nameIdentifier': {
            'nameIdentifier': '1234',
            'schemeURI': 'http://orcid.org',
            'nameIdentifierScheme': 'orcid',
        },
    }]})
    assert len(tree.xpath(
        '/resource/contributors/contributor/contributorName')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/nameIdentifier')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/affiliation')) == 1


def test_dates():
    """Test publisher."""
    tree = dump_etree({'dates': []})
    assert len(tree.xpath('/resource/dates')) == 0

    pytest.raises(KeyError, dump_etree, {'dates': [{'date': '2011-01-01'}]})

    elem = dump_etree({'dates': [
        {'date': '2011-01-01', 'dateType': 'Accepted'}
    ]}).xpath('/resource/dates/date')[0]
    assert elem.text == '2011-01-01'
    assert elem.get('dateType') == 'Accepted'


def test_language():
    """Test language."""
    tree = dump_etree({'language': 'en'})
    assert tree.xpath('/resource/language')[0].text == 'en'

    tree = dump_etree({'language': ''})
    assert len(tree.xpath('/resource/language')) == 0


def test_resourcetype():
    """Test resource type."""
    tree = dump_etree({'resourceType': {}})
    assert len(tree.xpath('/resource/resourceType')) == 0

    elem = dump_etree({'resourceType': {
        'resourceTypeGeneral': 'Software'
    }}).xpath('/resource/resourceType')[0]
    assert elem.get('resourceTypeGeneral') == 'Software'
    assert elem.text is None

    pytest.raises(KeyError, dump_etree, {'resourceType': {
        'resourceType': 'Science Software'
    }})

    elem = dump_etree({'resourceType': {
        'resourceTypeGeneral': 'Software',
        'resourceType': 'Science Software'
    }}).xpath('/resource/resourceType')[0]
    assert elem.get('resourceTypeGeneral') == 'Software'
    assert elem.text == 'Science Software'


def test_alternateidentifiers():
    """Test publisher."""
    pytest.raises(TypeError, dump_etree, {'alternateIdentifiers': {
        'invalid': 'data'
    }})

    tree = dump_etree({'alternateIdentifiers': []})
    assert len(tree.xpath('/resource/alternateIdentifiers')) == 0

    elem = dump_etree({'alternateIdentifiers': [
        {
            'alternateIdentifier': '10.1234/foo',
            'alternateIdentifierType': 'DOI',
        },
    ]}).xpath('/resource/alternateIdentifiers/alternateIdentifier')[0]
    assert elem.get('alternateIdentifierType') == 'DOI'
    assert elem.text == '10.1234/foo'


def test_relatedidentifiers():
    """Test publisher."""
    tree = dump_etree({'relatedIdentifiers': []})
    assert len(tree.xpath('/resource/relatedIdentifiers')) == 0

    elem = dump_etree({'relatedIdentifiers': [
        {
            'relatedIdentifier': '10.1234/foo',
            'relatedIdentifierType': 'DOI',
            'relationType': 'Cites'
        },
    ]}).xpath('/resource/relatedIdentifiers/relatedIdentifier')[0]
    assert elem.get('relatedIdentifierType') == 'DOI'
    assert elem.get('relationType') == 'Cites'
    assert elem.text == '10.1234/foo'

    elem = dump_etree({'relatedIdentifiers': [
        {
            'relatedIdentifier': '10.1234/foo',
            'relatedIdentifierType': 'DOI',
            'relationType': 'HasMetadata',
            'relatedMetadataScheme': 'MARC21',
            'schemeURI': 'http://loc.gov',
            'schemeType': 'XSD',
        },
    ]}).xpath('/resource/relatedIdentifiers/relatedIdentifier')[0]
    assert elem.get('relatedMetadataScheme') == 'MARC21'
    assert elem.get('schemeURI') == 'http://loc.gov'
    assert elem.get('schemeType') == 'XSD'


def test_sizes():
    """Test sizes."""
    tree = dump_etree({'sizes': []})
    assert len(tree.xpath('/resource/sizes')) == 0

    elem = dump_etree({'sizes': ['123']}).xpath('/resource/sizes/size')[0]
    assert elem.text == '123'


def test_formats():
    """Test formats."""
    tree = dump_etree({'formats': []})
    assert len(tree.xpath('/resource/formats')) == 0

    elem = dump_etree(
        {'formats': ['abc']}).xpath('/resource/formats/format')[0]
    assert elem.text == 'abc'


def test_version():
    """Test formats."""
    tree = dump_etree({'version': ''})
    assert len(tree.xpath('/resource/version')) == 0

    elem = dump_etree(
        {'version': 'v3.1'}).xpath('/resource/version')[0]
    assert elem.text == 'v3.1'


def test_rights():
    """Test publisher."""
    tree = dump_etree({'rightsList': []})
    assert len(tree.xpath('/resource/rightsList')) == 0

    elem = dump_etree({'rightsList': [
        {
            'rights': 'CC',
            'rightsURI': 'http://cc.org',
        },
    ]}).xpath('/resource/rightsList/rights')[0]
    assert elem.get('rightsURI') == 'http://cc.org'
    assert elem.text == 'CC'


def test_descriptions():
    """Test publisher."""
    tree = dump_etree({'descriptions': []})
    assert len(tree.xpath('/resource/descriptions')) == 0

    elem = dump_etree({'descriptions': [
        {
            'description': 'Test',
            'descriptionType': 'Abstract',
        },
    ]}).xpath('/resource/descriptions/description')[0]
    assert elem.get('descriptionType') == 'Abstract'
    assert elem.text == 'Test'


def test_geolocations():
    """Test publisher."""
    tree = dump_etree({'geoLocations': []})
    assert len(tree.xpath('/resource/geoLocations')) == 0

    elem = dump_etree({'geoLocations': [{
        'geoLocationPoint': '31 67',
        'geoLocationBox': '31 67 32 68',
        'geoLocationPlace': 'Atlantic Ocean',
    }, ]}).xpath('/resource/geoLocations/geoLocation')[0]
    point = elem.xpath('geoLocationPoint')[0]
    assert point.text == '31 67'
    box = elem.xpath('geoLocationBox')[0]
    assert box.text == '31 67 32 68'
    place = elem.xpath('geoLocationPlace')[0]
    assert place.text == 'Atlantic Ocean'


def test_minimal_xsd(xsd31):
    """Test that example XML converts to example JSON."""
    xsd31.assertValid(etree.XML(tostring({
        'identifier': {
            'identifierType': 'DOI',
            'identifier': '10.1234/foo.bar',
        },
        'creators': [
            {'creatorName': 'Nielsen, Lars Holm', },
            {
                'creatorName': 'Nielsen, Lars Holm',
                'nameIdentifier': {
                    'nameIdentifier': '1234',
                    'schemeURI': 'http://orcid.org',
                    'nameIdentifierScheme': 'ORCID',
                }
            }
        ],
        'titles': [
            {'title': 'Minimal Test Case', }
        ],
        'publisher': 'Invenio Software',
        'publicationYear': '2016',
    }).encode('utf8')))


def test_minimal_xml(xsd31):
    """Test minimal xml."""
    from lxml import etree
    xml = """
    <resource
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns="http://datacite.org/schema/kernel-3"
     xsi:schemaLocation="http://datacite.org/schema/kernel-3
      http://schema.datacite.org/meta/kernel-3/metadata.xsd">
        <identifier identifierType="DOI">10.1234/foo.bar</identifier>
        <creators>
            <creator><creatorName>Nielsen, Lars Holm</creatorName></creator>
        </creators>
        <titles>
            <title>Minimal Test Case</title>
        </titles>
        <publisher>Invenio Software</publisher>
        <publicationYear>2016</publicationYear>
    </resource>"""
    xsd31.assertValid(etree.XML(xml))
