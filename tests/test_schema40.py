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

from datacite.schema40 import dump_etree, tostring, validate


def test_example_json_validates(example_json40):
    """Test the example file validates against the JSON schema."""
    assert validate(example_json40)


def test_json_to_xml(example_xml_file40, example_json40, xsd40):
    """Test that example XML converts to example JSON."""
    xsd40.assertValid(etree.XML(example_xml_file40.encode('utf8')))
    xsd40.assertValid(etree.XML(tostring(example_json40).encode('utf8')))


def test_identifier():
    """Test identifier."""
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
        'familyName': 'Smith',
        'givenName': 'John',
        'affiliations': ['CERN', 'TIND'],
        'nameIdentifiers': [
            {
                'nameIdentifier': '1234',
                'schemeURI': 'http://orcid.org',
                'nameIdentifierScheme': 'orcid',
            },
        ]
    }]})
    assert len(tree.xpath('/resource/creators/creator/creatorName')) == 1
    assert len(tree.xpath('/resource/creators/creator/familyName')) == 1
    assert len(tree.xpath('/resource/creators/creator/givenName')) == 1
    assert len(tree.xpath('/resource/creators/creator/nameIdentifier')) == 1
    assert len(tree.xpath('/resource/creators/creator/affiliation')) == 2


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
    """Test publication year."""
    tree = dump_etree({'publicationYear': 2002})
    assert tree.xpath('/resource/publicationYear')[0].text == '2002'

    tree = dump_etree({'publicationYear': None})
    assert len(tree.xpath('/resource/publicationYear')) == 0


def test_subjects():
    """Test subjects."""
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
        'valueURI': 'https://cern.ch'
    }]}).xpath('/resource/subjects/subject')[0]
    assert elem.text == 'test'
    assert elem.get('subjectScheme') == 'dewey'
    assert elem.get('schemeURI') == 'dewey-uri'
    assert elem.get('valueURI') == 'https://cern.ch'


def test_contributors():
    """Test contributors."""
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
        'familyName': 'Smith',
        'givenName': 'John',
        'contributorType': 'Funder',
        'affiliations': ['CERN'],
        'nameIdentifiers': [
            {
                'nameIdentifier': '1234',
                'schemeURI': 'http://orcid.org',
                'nameIdentifierScheme': 'orcid',
            },
        ]
    }]})
    assert len(tree.xpath(
        '/resource/contributors/contributor/contributorName')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/familyName')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/givenName')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/nameIdentifier')) == 1
    assert len(tree.xpath(
        '/resource/contributors/contributor/affiliation')) == 1


def test_dates():
    """Test dates."""
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
    """Test alternate identifiers."""
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
    """Test related identifiers."""
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
    """Test version."""
    tree = dump_etree({'version': ''})
    assert len(tree.xpath('/resource/version')) == 0

    elem = dump_etree(
        {'version': 'v3.1'}).xpath('/resource/version')[0]
    assert elem.text == 'v3.1'


def test_rights():
    """Test rights."""
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
    """Test descriptions."""
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


def test_fundingreferences():
    """Test funding references."""
    tree = dump_etree({'fundingReferences': []})
    assert len(tree.xpath('/resource/fundingReferences')) == 0

    elem = dump_etree({'fundingReferences': [{
        'funderName': 'funderName',
        'funderIdentifier': {
            'funderIdentifier': 'id',
            'funderIdentifierType': 'ISNI'
        },
        'awardNumber': {
            'awardNumber': '282625',
            'awardURI': 'https://cern.ch'
        },
        'awardTitle': 'title'
    }, ]}).xpath('/resource/fundingReferences/fundingReference')[0]
    name = elem.xpath('funderName')[0]
    assert name.text == 'funderName'
    id = elem.xpath('funderIdentifier')[0]
    assert id.text == 'id'
    assert id.get('funderIdentifierType') == 'ISNI'
    award = elem.xpath('awardNumber')[0]
    assert award.text == '282625'
    assert award.get('awardURI') == 'https://cern.ch'
    title = elem.xpath('awardTitle')[0]
    assert title.text == 'title'


def test_geolocations():
    """Test geolocation."""
    tree = dump_etree({'geoLocations': []})
    assert len(tree.xpath('/resource/geoLocations')) == 0

    elem = dump_etree({'geoLocations': [{
        'geoLocationPoint': {
            'pointLongitude': 31.12,
            'pointLatitude': 67
        },
        'geoLocationBox': {
            'westBoundLongitude': 31.12,
            'eastBoundLongitude': 67,
            'southBoundLatitude': 32,
            'northBoundLatitude': 68
        },
        'geoLocationPlace': 'Atlantic Ocean',
        'geoLocationPolygon': {
            'polygonPoints': [
                {
                    'pointLongitude': 31.12,
                    'pointLatitude': 67
                },
                {
                    'pointLongitude': 32,
                    'pointLatitude': 68
                },
                {
                    'pointLongitude': 31.12,
                    'pointLatitude': 67
                },
            ]
        }
    }, ]}).xpath('/resource/geoLocations/geoLocation')[0]
    pointlong = elem.xpath('geoLocationPoint/pointLongitude')[0]
    pointlat = elem.xpath('geoLocationPoint/pointLatitude')[0]
    assert pointlong.text == '31.12'
    assert pointlat.text == '67'
    boxwest = elem.xpath('geoLocationBox/westBoundLongitude')[0]
    boxest = elem.xpath('geoLocationBox/eastBoundLongitude')[0]
    boxsouth = elem.xpath('geoLocationBox/southBoundLatitude')[0]
    boxnorth = elem.xpath('geoLocationBox/northBoundLatitude')[0]
    assert boxwest.text == '31.12'
    assert boxest.text == '67'
    assert boxsouth.text == '32'
    assert boxnorth.text == '68'
    place = elem.xpath('geoLocationPlace')[0]
    assert place.text == 'Atlantic Ocean'
    points = elem.xpath('geoLocationPolygon')[0]
    p1long = points[0].xpath('pointLongitude')[0]
    p1lat = points[0].xpath('pointLatitude')[0]
    p2long = points[1].xpath('pointLongitude')[0]
    p2lat = points[1].xpath('pointLatitude')[0]
    p3long = points[2].xpath('pointLongitude')[0]
    p3lat = points[2].xpath('pointLatitude')[0]
    assert p1long.text == '31.12'
    assert p1lat.text == '67'
    assert p2long.text == '32'
    assert p2lat.text == '68'
    assert p3long.text == '31.12'
    assert p3lat.text == '67'


def test_minimal_xsd(xsd40):
    """Test that example XML converts to example JSON."""
    xsd40.assertValid(etree.XML(tostring({
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
        'resourceType': {
            'resourceTypeGeneral': 'Dataset'
        }
    }).encode('utf8')))


def test_minimal_xml(xsd40):
    """Test minimal xml."""
    xml = """
    <resource
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns="http://datacite.org/schema/kernel-4"
     xsi:schemaLocation="http://datacite.org/schema/kernel-4
      http://schema.datacite.org/meta/kernel-4/metadata.xsd">
        <identifier identifierType="DOI">10.1234/foo.bar</identifier>
        <creators>
            <creator><creatorName>Nielsen, Lars Holm</creatorName></creator>
        </creators>
        <titles>
            <title>Minimal Test Case</title>
        </titles>
        <publisher>Invenio Software</publisher>
        <publicationYear>2016</publicationYear>
        <resourceType resourceTypeGeneral="Dataset"></resourceType>
    </resource>"""
    xsd40.assertValid(etree.XML(xml))
