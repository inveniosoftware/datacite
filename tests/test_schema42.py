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

"""Tests for format transformations."""

import xml.etree.ElementTree as ET
from os.path import dirname, join

import pytest
from helpers import load_json_path, load_xml_path
from lxml import etree

from datacite.schema42 import dump_etree, tostring, validate, validator
from datacite.xmlutils import etree_to_string


def validate_json(minimal_json, extra_json):
    """Validate specific property."""
    data = {}
    data.update(minimal_json)
    data.update(extra_json)
    validator.validate(data)


#
# Tests on example files
#
TEST_JSON_FILES = [
    "data/4.2/datacite-example-polygon-v4.json",
    "data/4.2/datacite-example-fundingReference-v4.json",
    "data/4.2/datacite-example-ResearchGroup_Methods-v4.json",
    "data/4.2/datacite-example-complicated-v4.json",
    "data/4.2/datacite-example-datapaper-v4.json",
    "data/4.2/datacite-example-video-v4.json",
    "data/4.2/datacite-example-dataset-v4.json",
    "data/4.2/datacite-example-Box_dateCollected_DataCollector-v4.json",
    "data/4.2/datacite-example-ResourceTypeGeneral_Collection-v4.json",
    "data/4.2/datacite-example-HasMetadata-v4.json",
    "data/4.2/datacite-example-workflow-v4.json",
    "data/4.2/datacite-example-full-v4.json",
    "data/4.2/datacite-example-GeoLocation-v4.json",
    "data/4.2/datacite-example-relationTypeIsIdenticalTo-v4.json",
    "data/4.2/datacite-example-software-v4.json",
    "data/4.2/datacite-example-DateRange-v4.json",
    "data/datacite-v4.2-full-example.json",
]


@pytest.mark.parametrize("example_json42", TEST_JSON_FILES)
def test_example_json_validates(example_json42):
    """Test the example file validates against the JSON schema."""
    example_json = load_json_path(example_json42)
    validator.validate(example_json)


FILE_PAIRS = [
    (
        "data/4.2/datacite-example-polygon-v4.xml",
        "data/4.2/datacite-example-polygon-v4.json",
    ),
    (
        "data/4.2/datacite-example-fundingReference-v4.xml",
        "data/4.2/datacite-example-fundingReference-v4.json",
    ),
    (
        "data/4.2/datacite-example-ResearchGroup_Methods-v4.xml",
        "data/4.2/datacite-example-ResearchGroup_Methods-v4.json",
    ),
    (
        "data/4.2/datacite-example-complicated-v4.xml",
        "data/4.2/datacite-example-complicated-v4.json",
    ),
    (
        "data/4.2/datacite-example-datapaper-v4.xml",
        "data/4.2/datacite-example-datapaper-v4.json",
    ),
    (
        "data/4.2/datacite-example-video-v4.xml",
        "data/4.2/datacite-example-video-v4.json",
    ),
    (
        "data/4.2/datacite-example-dataset-v4.xml",
        "data/4.2/datacite-example-dataset-v4.json",
    ),
    (
        "data/4.2/datacite-example-Box_dateCollected_DataCollector-v4.xml",
        "data/4.2/datacite-example-Box_dateCollected_DataCollector-v4.json",
    ),
    (
        "data/4.2/datacite-example-ResourceTypeGeneral_Collection-v4.xml",
        "data/4.2/datacite-example-ResourceTypeGeneral_Collection-v4.json",
    ),
    (
        "data/4.2/datacite-example-HasMetadata-v4.xml",
        "data/4.2/datacite-example-HasMetadata-v4.json",
    ),
    (
        "data/4.2/datacite-example-workflow-v4.xml",
        "data/4.2/datacite-example-workflow-v4.json",
    ),
    ("data/4.2/datacite-example-full-v4.xml", "data/4.2/datacite-example-full-v4.json"),
    (
        "data/4.2/datacite-example-GeoLocation-v4.xml",
        "data/4.2/datacite-example-GeoLocation-v4.json",
    ),
    (
        "data/4.2/datacite-example-relationTypeIsIdenticalTo-v4.xml",
        "data/4.2/datacite-example-relationTypeIsIdenticalTo-v4.json",
    ),
    (
        "data/4.2/datacite-example-software-v4.xml",
        "data/4.2/datacite-example-software-v4.json",
    ),
    (
        "data/4.2/datacite-example-DateRange-v4.xml",
        "data/4.2/datacite-example-DateRange-v4.json",
    ),
    ("data/datacite-v4.2-full-example.xml", "data/datacite-v4.2-full-example.json"),
]


@pytest.mark.parametrize("example_xml42, example_json42", FILE_PAIRS)
def test_json_to_xml(example_xml42, example_json42, xsd42):
    """Test that example XML converts to example JSON."""
    example_xml = load_xml_path(example_xml42)
    example_json = load_json_path(example_json42)
    xsd42.assertValid(etree.XML(example_xml.encode("utf8")))
    xsd42.assertValid(etree.XML(tostring(example_json).encode("utf8")))


def test_json_eq_xml(example_xml_file42, example_json42, xsd42):
    """Test that example XML converts to example JSON."""
    xsd42.assertValid(etree.XML(tostring(example_json42).encode("utf8")))


#
# Field by field tests.
#
def test_identifier(minimal_json42):
    """Test identifier."""
    data = {
        "identifiers": [
            {
                "identifierType": "DOI",
                "identifier": "10.1234/foo.bar",
            }
        ]
    }
    validate_json(minimal_json42, data)
    tree = dump_etree(data)
    elem = tree.xpath("/resource/identifier")[0]
    assert elem.text == "10.1234/foo.bar"
    assert elem.get("identifierType") == "DOI"


def test_creators(minimal_json42):
    """Test creators."""
    pytest.raises(TypeError, dump_etree, {"creators": {"invalid": "data"}})

    tree = dump_etree({"creators": []})
    assert len(tree.xpath("/resource/creators")) == 0

    tree = dump_etree(
        {
            "creators": [
                {
                    "name": "Smith, John",
                }
            ]
        }
    )
    assert len(tree.xpath("/resource/creators/creator")) == 1
    assert len(tree.xpath("/resource/creators/creator/creatorName")) == 1
    assert len(tree.xpath("/resource/creators/creator/nameIdentifier")) == 0
    assert len(tree.xpath("/resource/creators/creator/affiliation")) == 0

    data = {
        "creators": [
            {
                "name": "Smith, John",
                "familyName": "Smith",
                "givenName": "John",
                "affiliations": [{"affiliation": "CERN"}, {"affiliation": "TIND"}],
                "nameIdentifiers": [
                    {
                        "nameIdentifier": "1234",
                        "schemeURI": "http://orcid.org",
                        "nameIdentifierScheme": "orcid",
                    },
                ],
            }
        ]
    }
    validate_json(minimal_json42, data)

    tree = dump_etree(data)
    assert len(tree.xpath("/resource/creators/creator/creatorName")) == 1
    assert len(tree.xpath("/resource/creators/creator/familyName")) == 1
    assert len(tree.xpath("/resource/creators/creator/givenName")) == 1
    assert len(tree.xpath("/resource/creators/creator/nameIdentifier")) == 1
    assert len(tree.xpath("/resource/creators/creator/affiliation")) == 2


def test_titles(minimal_json42):
    """Test titles."""
    pytest.raises(TypeError, dump_etree, {"titles": {"invalid": "data"}})

    tree = dump_etree({"titles": []})
    assert len(tree.xpath("/resource/titles")) == 0

    tree = dump_etree({"titles": [{"title": "Test"}]})
    assert len(tree.xpath("/resource/titles")) == 1
    assert len(tree.xpath("/resource/titles/title")) == 1

    data = {"titles": [{"title": "Test", "titleType": "Subtitle"}]}
    validate_json(minimal_json42, data)

    elem = dump_etree(data).xpath("/resource/titles/title")[0]
    assert elem.text == "Test"
    assert elem.get("titleType") == "Subtitle"

    elem = dump_etree({"titles": [{"title": "Test", "lang": "en"}]}).xpath(
        "/resource/titles/title"
    )[0]
    assert elem.get("{xml}lang") == "en"


def test_publisher(minimal_json42):
    """Test publisher."""
    data = {"publisher": "test"}
    validate_json(minimal_json42, data)
    tree = dump_etree(data)
    assert tree.xpath("/resource/publisher")[0].text == "test"

    tree = dump_etree({"publisher": ""})
    assert len(tree.xpath("/resource/publisher")) == 0


def test_publicationyear(minimal_json42):
    """Test publication year."""
    data = {"publicationYear": "2002"}
    validate_json(minimal_json42, data)
    tree = dump_etree(data)
    assert tree.xpath("/resource/publicationYear")[0].text == "2002"

    tree = dump_etree({"publicationYear": None})
    assert len(tree.xpath("/resource/publicationYear")) == 0


def test_subjects(minimal_json42):
    """Test subjects."""
    pytest.raises(TypeError, dump_etree, {"subjects": {"invalid": "data"}})

    tree = dump_etree({"subjects": []})
    assert len(tree.xpath("/resource/subjects")) == 0

    tree = dump_etree({"subjects": [{"subject": "test"}]})
    assert len(tree.xpath("/resource/subjects/subject")) == 1

    data = {
        "subjects": [
            {
                "subject": "test",
                "subjectScheme": "dewey",
                "schemeURI": "dewey-uri",
                "valueURI": "https://cern.ch",
            }
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/subjects/subject")[0]
    assert elem.text == "test"
    assert elem.get("subjectScheme") == "dewey"
    assert elem.get("schemeURI") == "dewey-uri"
    assert elem.get("valueURI") == "https://cern.ch"


def test_contributors(minimal_json42):
    """Test contributors."""
    pytest.raises(TypeError, dump_etree, {"contributors": {"invalid": "data"}})

    tree = dump_etree({"contributors": []})
    assert len(tree.xpath("/resource/contributors")) == 0

    tree = dump_etree(
        {
            "contributors": [
                {
                    "name": "CERN",
                    "nameType": "Organisational",
                    "contributorType": "HostingInstitution",
                }
            ]
        }
    )
    assert len(tree.xpath("/resource/contributors/contributor")) == 1
    assert len(tree.xpath("/resource/contributors/contributor/contributorName")) == 1
    cntr1 = tree.xpath("/resource/contributors/contributor/contributorName")[0]
    assert cntr1.attrib["nameType"] == "Organisational"
    assert len(tree.xpath("/resource/contributors/contributor/nameIdentifier")) == 0
    assert len(tree.xpath("/resource/contributors/contributor/affiliation")) == 0

    data = {
        "contributors": [
            {
                "name": "Smith, John",
                "nameType": "Personal",
                "familyName": "Smith",
                "givenName": "John",
                "contributorType": "ContactPerson",
                "affiliations": [{"affiliation": "CERN"}],
                "nameIdentifiers": [
                    {
                        "nameIdentifier": "1234",
                        "schemeURI": "http://orcid.org",
                        "nameIdentifierScheme": "orcid",
                    },
                ],
            }
        ]
    }
    validate_json(minimal_json42, data)

    tree = dump_etree(data)
    assert len(tree.xpath("/resource/contributors/contributor/contributorName")) == 1
    cntr1 = tree.xpath("/resource/contributors/contributor/contributorName")[0]
    assert cntr1.attrib["nameType"] == "Personal"
    assert len(tree.xpath("/resource/contributors/contributor/familyName")) == 1
    assert len(tree.xpath("/resource/contributors/contributor/givenName")) == 1
    assert len(tree.xpath("/resource/contributors/contributor/nameIdentifier")) == 1
    assert len(tree.xpath("/resource/contributors/contributor/affiliation")) == 1


def test_dates(minimal_json42):
    """Test dates."""
    tree = dump_etree({"dates": []})
    assert len(tree.xpath("/resource/dates")) == 0

    pytest.raises(KeyError, dump_etree, {"dates": [{"date": "2011-01-01"}]})

    data = {
        "dates": [
            {
                "date": "2011-01-01",
                "dateType": "Accepted",
                "dateInformation": "Date of paper acceptance.",
            }
        ]
    }
    validate_json(minimal_json42, data)

    elem = dump_etree(data).xpath("/resource/dates/date")[0]
    assert elem.text == "2011-01-01"
    assert elem.get("dateType") == "Accepted"
    assert elem.get("dateInformation") == "Date of paper acceptance."


def test_language(minimal_json42):
    """Test language."""
    data = {"language": "en"}
    validate_json(minimal_json42, data)
    tree = dump_etree(data)
    assert tree.xpath("/resource/language")[0].text == "en"

    tree = dump_etree({"language": ""})
    assert len(tree.xpath("/resource/language")) == 0


def test_resourcetype(minimal_json42):
    """Test resource type."""
    data = {
        "types": {"resourceTypeGeneral": "Software", "resourceType": "Science Software"}
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/resourceType")[0]
    assert elem.get("resourceTypeGeneral") == "Software"
    assert elem.text == "Science Software"


def test_identifiers(minimal_json42):
    """Test identifiers."""
    pytest.raises(TypeError, dump_etree, {"identifiers": {"invalid": "data"}})

    data = {"identifiers": [{"identifier": "10.1234/foo", "identifierType": "DOI"}]}
    validate_json(minimal_json42, data)
    tree = dump_etree(data)
    elem = dump_etree(data).xpath("/resource/identifier")[0]
    assert elem.get("identifierType") == "DOI"
    assert elem.text == "10.1234/foo"

    data = {
        "identifiers": [
            {
                "identifier": "10.1234/foo",
                "identifierType": "DOI",
            },
            {"identifierType": "internal ID", "identifier": "da|ra.14.103"},
        ]
    }
    validate_json(minimal_json42, data)

    elem = dump_etree(data).xpath("/resource/alternateIdentifiers/alternateIdentifier")[
        0
    ]
    assert elem.get("alternateIdentifierType") == "internal ID"
    assert elem.text == "da|ra.14.103"
    elem = dump_etree(data).xpath("/resource/identifier")[0]
    assert elem.get("identifierType") == "DOI"
    assert elem.text == "10.1234/foo"

    data = {"identifiers": [{"identifier": "13682", "identifierType": "Eprint_ID"}]}

    xml = tostring(data)
    elem = dump_etree(data).xpath("/resource/alternateIdentifiers/alternateIdentifier")[
        0
    ]
    assert elem.get("alternateIdentifierType") == "Eprint_ID"
    assert elem.text == "13682"


def test_relatedidentifiers(minimal_json42):
    """Test related identifiers."""
    tree = dump_etree({"relatedIdentifiers": []})
    assert len(tree.xpath("/resource/relatedIdentifiers")) == 0

    data = {
        "relatedIdentifiers": [
            {
                "relatedIdentifier": "10.1234/foo",
                "relatedIdentifierType": "DOI",
                "relationType": "Cites",
            },
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/relatedIdentifiers/relatedIdentifier")[0]
    assert elem.get("relatedIdentifierType") == "DOI"
    assert elem.get("relationType") == "Cites"
    assert elem.text == "10.1234/foo"

    data = {
        "relatedIdentifiers": [
            {
                "relatedIdentifier": "10.1234/foo",
                "relatedIdentifierType": "DOI",
                "relationType": "HasMetadata",
                "relatedMetadataScheme": "MARC21",
                "schemeURI": "http://loc.gov",
                "schemeType": "XSD",
                "resourceTypeGeneral": "Software",
            },
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/relatedIdentifiers/relatedIdentifier")[0]
    assert elem.get("relatedMetadataScheme") == "MARC21"
    assert elem.get("schemeURI") == "http://loc.gov"
    assert elem.get("schemeType") == "XSD"
    assert elem.get("resourceTypeGeneral") == "Software"


def test_sizes(minimal_json42):
    """Test sizes."""
    tree = dump_etree({"sizes": []})
    assert len(tree.xpath("/resource/sizes")) == 0

    data = {"sizes": ["123"]}
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/sizes/size")[0]
    assert elem.text == "123"


def test_formats(minimal_json42):
    """Test formats."""
    tree = dump_etree({"formats": []})
    assert len(tree.xpath("/resource/formats")) == 0

    data = {"formats": ["abc"]}
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/formats/format")[0]
    assert elem.text == "abc"


def test_version(minimal_json42):
    """Test version."""
    tree = dump_etree({"version": ""})
    assert len(tree.xpath("/resource/version")) == 0

    data = {"version": "v3.1"}
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/version")[0]
    assert elem.text == "v3.1"


def test_rights(minimal_json42):
    """Test rights."""
    tree = dump_etree({"rightsList": []})
    assert len(tree.xpath("/resource/rightsList")) == 0

    data = {
        "rightsList": [
            {"rights": "CC", "rightsURI": "http://cc.org", "lang": "en"},
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/rightsList/rights")[0]
    assert elem.get("rightsURI") == "http://cc.org"
    assert elem.get("{xml}lang") == "en"
    assert elem.text == "CC"


def test_descriptions(minimal_json42):
    """Test descriptions."""
    tree = dump_etree({"descriptions": []})
    assert len(tree.xpath("/resource/descriptions")) == 0

    data = {
        "descriptions": [
            {
                "description": "Test",
                "descriptionType": "Abstract",
            },
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/descriptions/description")[0]
    assert elem.get("descriptionType") == "Abstract"
    assert elem.text == "Test"


def test_fundingreferences(minimal_json42):
    """Test funding references."""
    tree = dump_etree({"fundingReferences": []})
    assert len(tree.xpath("/resource/fundingReferences")) == 0

    data = {
        "fundingReferences": [
            {
                "funderName": "funderName",
                "funderIdentifier": "id",
                "funderIdentifierType": "ISNI",
                "awardNumber": "282625",
                "awardURI": "https://cern.ch",
                "awardTitle": "title",
            },
        ]
    }
    validate_json(minimal_json42, data)
    elem = dump_etree(data).xpath("/resource/fundingReferences/fundingReference")[0]
    name = elem.xpath("funderName")[0]
    assert name.text == "funderName"
    id = elem.xpath("funderIdentifier")[0]
    assert id.text == "id"
    assert id.get("funderIdentifierType") == "ISNI"
    award = elem.xpath("awardNumber")[0]
    assert award.text == "282625"
    assert award.get("awardURI") == "https://cern.ch"
    title = elem.xpath("awardTitle")[0]
    assert title.text == "title"


def test_geolocations(minimal_json42):
    """Test geolocation."""
    tree = dump_etree({"geoLocations": []})
    assert len(tree.xpath("/resource/geoLocations")) == 0

    data = {
        "geoLocations": [
            {
                "geoLocationPoint": {"pointLongitude": "31.12", "pointLatitude": "67"},
                "geoLocationBox": {
                    "westBoundLongitude": "31.12",
                    "eastBoundLongitude": "67",
                    "southBoundLatitude": "32",
                    "northBoundLatitude": "68",
                },
                "geoLocationPlace": "Atlantic Ocean",
                "geoLocationPolygons": [
                    {
                        "polygonPoints": [
                            {"pointLongitude": "-71.032", "pointLatitude": "41.090"},
                            {"pointLongitude": "-68.211", "pointLatitude": "42.893"},
                            {"pointLongitude": "-72.032", "pointLatitude": "39.090"},
                            {"pointLongitude": "-71.032", "pointLatitude": "41.090"},
                        ]
                    },
                    {
                        "polygonPoints": [
                            {"pointLongitude": "-72.032", "pointLatitude": "42.090"},
                            {"pointLongitude": "-69.211", "pointLatitude": "43.893"},
                            {"pointLongitude": "-73.032", "pointLatitude": "41.090"},
                            {"pointLongitude": "-72.032", "pointLatitude": "42.090"},
                        ],
                        "inPolygonPoint": {
                            "pointLongitude": "-52.032",
                            "pointLatitude": "12.090",
                        },
                    },
                ],
            }
        ]
    }
    validate_json(minimal_json42, data)

    elem = dump_etree(data).xpath("/resource/geoLocations/geoLocation")[0]
    pointlong = elem.xpath("geoLocationPoint/pointLongitude")[0]
    pointlat = elem.xpath("geoLocationPoint/pointLatitude")[0]
    assert pointlong.text == "31.12"
    assert pointlat.text == "67"
    boxwest = elem.xpath("geoLocationBox/westBoundLongitude")[0]
    boxest = elem.xpath("geoLocationBox/eastBoundLongitude")[0]
    boxsouth = elem.xpath("geoLocationBox/southBoundLatitude")[0]
    boxnorth = elem.xpath("geoLocationBox/northBoundLatitude")[0]
    assert boxwest.text == "31.12"
    assert boxest.text == "67"
    assert boxsouth.text == "32"
    assert boxnorth.text == "68"
    place = elem.xpath("geoLocationPlace")[0]
    assert place.text == "Atlantic Ocean"
    polygons = elem.xpath("geoLocationPolygon")
    assert len(polygons) == 2
    # Polygon 1
    points = polygons[0]
    assert len(points) == 4
    p1long = points[0].xpath("pointLongitude")[0]
    p1lat = points[0].xpath("pointLatitude")[0]
    p2long = points[1].xpath("pointLongitude")[0]
    p2lat = points[1].xpath("pointLatitude")[0]
    p3long = points[2].xpath("pointLongitude")[0]
    p3lat = points[2].xpath("pointLatitude")[0]
    p4long = points[3].xpath("pointLongitude")[0]
    p4lat = points[3].xpath("pointLatitude")[0]
    assert p1long.text == "-71.032"
    assert p1lat.text == "41.090"
    assert p2long.text == "-68.211"
    assert p2lat.text == "42.893"
    assert p3long.text == "-72.032"
    assert p3lat.text == "39.090"
    assert p4long.text == "-71.032"
    assert p4lat.text == "41.090"
    # Polygon 2
    points = polygons[1]
    assert len(points) == 5
    assert len(points.xpath("inPolygonPoint")) == 1
    assert len(points.xpath("polygonPoint")) == 4
    inp = points.xpath("inPolygonPoint")[0]
    inplat = inp.xpath("pointLatitude")[0]
    inplong = inp.xpath("pointLongitude")[0]
    assert inplat.text == "12.090"
    assert inplong.text == "-52.032"


#
# Additional tests
#
def test_minimal_xsd(xsd42, minimal_json42):
    """Test that example XML converts to example JSON."""
    validator.validate(minimal_json42)
    xsd42.assertValid(etree.XML(tostring(minimal_json42).encode("utf8")))


def test_minimal_xml(xsd42):
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
        <resourceType resourceTypeGeneral="Software"></resourceType>
    </resource>"""
    xsd42.assertValid(etree.XML(xml))


FIELD_NAMES = [
    "dates",
    "subjects",
    "contributors",
    "relatedIdentifiers",
    "sizes",
    "formats",
    "rightsList",
    "descriptions",
    "geoLocations",
    "fundingReferences",
]


@pytest.mark.parametrize("field_name", FIELD_NAMES)
def test_empty_arrays(xsd42, minimal_json42, field_name):
    """Test proper behavior with empty lists for certain fields."""
    minimal_json42[field_name] = []
    validator.validate(minimal_json42)
    xsd42.assertValid(etree.XML(tostring(minimal_json42).encode("utf8")))
