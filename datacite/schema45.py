# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2016 CERN.
# Copyright (C) 2019 Caltech.
# Copyright (C) 2024 IBT Czech Academy of Sciences.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""DataCite v4.5 JSON to XML transformations."""

import pkg_resources
from lxml import etree
from lxml.builder import E

from .jsonutils import validator_factory
from .xmlutils import (
    Rules,
    dump_etree_helper,
    etree_to_string,
    set_elem_attr,
    set_non_empty_attr,
)

rules = Rules()

ns = {
    None: "http://datacite.org/schema/kernel-4",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xml": "xml",
}

root_attribs = {
    "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://datacite.org/schema/kernel-4 "
    "http://schema.datacite.org/meta/kernel-4.5/metadata.xsd",
}

validator = validator_factory(
    pkg_resources.resource_filename("datacite", "schemas/datacite-v4.5.json")
)


def dump_etree(data):
    """Convert JSON dictionary to DataCite v4.5 XML as ElementTree."""
    return dump_etree_helper(data, rules, ns, root_attribs)


def tostring(data, **kwargs):
    """Convert JSON dictionary to DataCite v4.5 XML as string."""
    return etree_to_string(dump_etree(data), **kwargs)


def validate(data):
    """Validate DataCite v4.5 JSON dictionary."""
    return validator.is_valid(data)


def affiliation(root, values):
    """Extract affiliation."""
    vals = values.get("affiliation", [])
    for val in vals:
        if val.get("name"):
            elem = E.affiliation(val["name"])
            # affiliationIdentifier metadata as Attributes
            # (0-1 cardinality, instead of 0-n as list of objects)
            set_elem_attr(elem, "affiliationIdentifier", val)
            set_elem_attr(elem, "affiliationIdentifierScheme", val)
            if val.get("schemeUri"):
                elem.set("schemeURI", val["schemeUri"])
            root.append(elem)


def familyname(root, value):
    """Extract family name."""
    val = value.get("familyName")
    if val:
        root.append(E.familyName(val))


def givenname(root, value):
    """Extract family name."""
    val = value.get("givenName")
    if val:
        root.append(E.givenName(val))


def person_or_org_name(root, value, xml_tagname, json_tagname):
    """Extract creator/contributor name and it's 'nameType' attribute."""
    elem = E(xml_tagname, value[json_tagname])
    set_elem_attr(elem, "nameType", value)
    set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
    root.append(elem)


def nameidentifiers(root, values):
    """Extract nameidentifier."""
    vals = values.get("nameIdentifiers", [])
    for val in vals:
        if val.get("nameIdentifier"):
            elem = E.nameIdentifier(val["nameIdentifier"])
            elem.set("nameIdentifierScheme", val["nameIdentifierScheme"])
            if val.get("schemeUri"):
                elem.set("schemeURI", val["schemeUri"])
            root.append(elem)


def fetch_creator(root, value):
    """Extract common values for creator and contributor."""
    givenname(root, value)
    familyname(root, value)
    nameidentifiers(root, value)
    affiliation(root, value)


def title(root, values):
    """Extract titles."""
    if not values:
        return

    for value in values:
        elem = etree.Element("title", nsmap=ns)
        elem.text = value["title"]
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        # 'type' was a mistake in 4.0 serializer, which is supported
        # for backwards compatibility until kernel 5 is released.
        set_non_empty_attr(elem, "titleType", value.get("type"))
        # 'titleType' will supersede 'type' if available
        set_non_empty_attr(elem, "titleType", value.get("titleType"))
        root.append(elem)


def related_object(root, value):
    """Extract attributes of relatedIdentifiers and relatedItems."""
    if not value:
        return

    set_elem_attr(root, "relatedMetadataScheme", value)
    if value.get("schemeUri"):
        root.set("schemeURI", value["schemeUri"])
    set_elem_attr(root, "schemeType", value)
    set_elem_attr(root, "resourceTypeGeneral", value)


@rules.rule("alternateIdentifiers")
def alternate_identifiers(path, values):
    """Transform to alternateIdentifiers.

    Note that as of version schema 4.5 the identifiers field is deprecated
    in favour of using alternateIdentifiers and the doi field.
    """
    if not values:
        return

    root = E.alternateIdentifiers()
    for value in values:
        elem = E.alternateIdentifier(value["alternateIdentifier"])
        set_non_empty_attr(
            elem, "alternateIdentifierType", value.get("alternateIdentifierType")
        )
        root.append(elem)
    return root


@rules.rule("creators")
def creators(path, values):
    """Transform creators."""
    if not values:
        return

    root = E.creators()
    for value in values:
        creator = E.creator()
        person_or_org_name(creator, value, "creatorName", "name")
        fetch_creator(creator, value)
        root.append(creator)

    return root


@rules.rule("titles")
def titles(path, values):
    """Transform titles."""
    if not values:
        return
    root = E.titles()
    title(root, values)
    return root


@rules.rule("publisher")
def publisher(path, value):
    """Transform publisher."""
    if not value:
        return

    elem = E.publisher(value.get("name"))
    set_non_empty_attr(elem, "publisherIdentifier", value.get("publisherIdentifier"))
    set_non_empty_attr(
        elem, "publisherIdentifierScheme", value.get("publisherIdentifierScheme")
    )
    set_non_empty_attr(elem, "schemeURI", value.get("schemeUri"))

    return elem


@rules.rule("publicationYear")
def publication_year(path, value):
    """Transform publicationYear."""
    if not value:
        return
    return E.publicationYear(value)


@rules.rule("subjects")
def subjects(path, values):
    """Transform subjects."""
    if not values:
        return

    root = E.subjects()
    for value in values:
        elem = E.subject(value["subject"])
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        set_elem_attr(elem, "subjectScheme", value)
        if value.get("schemeUri"):
            elem.set("schemeURI", value["schemeUri"])
        if value.get("valueUri"):
            elem.set("valueURI", value["valueUri"])
        root.append(elem)
    return root


@rules.rule("contributors")
def contributors(path, values):
    """Transform contributors."""
    if not values:
        return

    root = E.contributors()
    for value in values:
        contributor = E.contributor()
        person_or_org_name(contributor, value, "contributorName", "name")
        fetch_creator(contributor, value)
        set_elem_attr(contributor, "contributorType", value)
        root.append(contributor)

    return root


@rules.rule("dates")
def dates(path, values):
    """Transform dates."""
    if not values:
        return

    root = E.dates()
    for value in values:
        elem = E.date(value["date"], dateType=value["dateType"])
        set_elem_attr(elem, "dateInformation", value)
        root.append(elem)

    return root


@rules.rule("language")
def language(path, value):
    """Transform language."""
    if not value:
        return
    return E.language(value)


@rules.rule("types")
def resource_type(path, value):
    """Transform resourceType."""
    elem = E.resourceType()
    elem.set("resourceTypeGeneral", value["resourceTypeGeneral"])
    elem.text = value.get("resourceType")
    return elem


@rules.rule("doi")
def identifier(path, value):
    """Transform doi into identifier."""
    if not value:
        return None

    return E.identifier(value, identifierType="DOI")


@rules.rule("relatedIdentifiers")
def related_identifiers(path, values):
    """Transform relatedIdentifiers."""
    if not values:
        return

    root = E.relatedIdentifiers()
    for value in values:
        elem = E.relatedIdentifier()
        elem.text = value["relatedIdentifier"]
        elem.set("relationType", value["relationType"])
        related_object(elem, value)
        set_elem_attr(elem, "relatedIdentifierType", value)
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


@rules.rule("sizes")
def sizes(path, values):
    """Transform sizes."""
    return free_text_list("sizes", "size", values)


@rules.rule("formats")
def formats(path, values):
    """Transform sizes."""
    return free_text_list("formats", "format", values)


@rules.rule("version")
def version(path, value):
    """Transform version."""
    if not value:
        return
    return E.version(value)


@rules.rule("rightsList")
def rights(path, values):
    """Transform rights."""
    if not values:
        return

    root = E.rightsList()
    for value in values:
        if "rights" in value:
            elem = E.rights(value["rights"])
        # Handle the odd case where no rights text present
        else:
            elem = E.rights()
        if value.get("rightsUri"):
            elem.set("rightsURI", value["rightsUri"])
        set_elem_attr(elem, "rightsIdentifierScheme", value)
        set_elem_attr(elem, "rightsIdentifier", value)
        if value.get("schemeUri"):
            elem.set("schemeURI", value["schemeUri"])
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        root.append(elem)
    return root


@rules.rule("descriptions")
def descriptions(path, values):
    """Transform descriptions."""
    if not values:
        return

    root = E.descriptions()
    for value in values:
        elem = E.description(
            value["description"], descriptionType=value["descriptionType"]
        )
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        root.append(elem)

    return root


def geopoint(root, value):
    """Extract a point (either geoLocationPoint or polygonPoint)."""
    root.append(E.pointLongitude(str(value["pointLongitude"])))
    root.append(E.pointLatitude(str(value["pointLatitude"])))


@rules.rule("geoLocations")
def geolocations(path, values):
    """Transform geolocations."""
    if not values:
        return

    root = E.geoLocations()
    for value in values:
        element = E.geoLocation()

        place = value.get("geoLocationPlace")
        if place:
            element.append(E.geoLocationPlace(place))

        point = value.get("geoLocationPoint")
        if point:
            elem = E.geoLocationPoint()
            geopoint(elem, point)
            element.append(elem)

        box = value.get("geoLocationBox")
        if box:
            elem = E.geoLocationBox()
            elem.append(E.westBoundLongitude(str(box["westBoundLongitude"])))
            elem.append(E.eastBoundLongitude(str(box["eastBoundLongitude"])))
            elem.append(E.southBoundLatitude(str(box["southBoundLatitude"])))
            elem.append(E.northBoundLatitude(str(box["northBoundLatitude"])))
            element.append(elem)

        polygon = value.get("geoLocationPolygon")
        if polygon:
            elem = E.geoLocationPolygon()
            for point in polygon:
                plainPoint = point.get("polygonPoint")
                if plainPoint:
                    e = E.polygonPoint()
                    geopoint(e, plainPoint)
                    elem.append(e)
                inPoint = point.get("inPolygonPoint")
                if inPoint:
                    e = E.inPolygonPoint()
                    geopoint(e, inPoint)
                    elem.append(e)
            element.append(elem)

        root.append(element)
    return root


@rules.rule("fundingReferences")
def fundingreferences(path, values):
    """Transform funding references."""
    if not values:
        return

    root = E.fundingReferences()
    for value in values:
        element = E.fundingReference()

        element.append(E.funderName(value.get("funderName")))

        identifier = value.get("funderIdentifier")
        if identifier:
            elem = E.funderIdentifier(identifier)
            typev = value.get("funderIdentifierType")
            if typev:
                elem.set("funderIdentifierType", typev)
            element.append(elem)

        number = value.get("awardNumber")
        if number:
            elem = E.awardNumber(number)
            uri = value.get("awardUri")
            if uri:
                elem.set("awardURI", uri)
            element.append(elem)

        title = value.get("awardTitle")
        if title:
            element.append(E.awardTitle(title))
        if len(element):
            root.append(element)
    return root


@rules.rule("relatedItems")
def related_items(path, values):
    """Transform related items."""
    if not values:
        return None
    pass

    root = E.relatedItems()
    for value in values:
        elem = E.relatedItem()
        set_elem_attr(elem, "relatedItemType", value)
        set_elem_attr(elem, "relationType", value)

        id_label = "relatedItemIdentifier"
        if value.get(id_label):
            related_item_identifier = E.relatedItemIdentifier()
            re_id = value[id_label]
            related_item_identifier.text = re_id[id_label]
            set_elem_attr(related_item_identifier, "relatedItemIdentifierType", re_id)
            related_object(related_item_identifier, value)
            elem.append(related_item_identifier)

        creator_values = value.get("creators")
        if creator_values:
            re_creators = E.creators()
            for c in creator_values:
                creator = E.creator()
                person_or_org_name(creator, c, "creatorName", "name")
                fetch_creator(creator, c)
                re_creators.append(creator)
            elem.append(re_creators)

        related_titles = E.titles()
        title(related_titles, value.get("titles"))
        elem.append(related_titles)

        pub_year = value.get("publicationYear")
        if pub_year:
            elem.append(E.publicationYear(pub_year))

        vol = value.get("volume")
        if vol:
            elem.append(E.volume(vol))

        issue = value.get("issue")
        if issue:
            elem.append(E.issue(issue))

        number = value.get("number")
        if number:
            re_number = E.number(number)
            if value.get("numberType"):
                set_elem_attr(re_number, "numberType", value)
            elem.append(re_number)

        first_p = value.get("firstPage")
        if first_p:
            elem.append(E.firstPage(first_p))

        last_p = value.get("lastPage")
        if last_p:
            elem.append(E.lastPage(last_p))

        pub = value.get("publisher")
        if pub:
            elem.append(E.publisher(pub))

        edi = value.get("edition")
        if edi:
            elem.append(E.edition(edi))

        contributors_values = value.get("contributors")
        if contributors_values:
            re_contributors = E.contributors()
            for c in contributors_values:
                contributor = E.contributor()
                person_or_org_name(contributor, c, "contributorName", "name")
                fetch_creator(contributor, c)
                set_elem_attr(contributor, "contributorType", c)
                re_contributors.append(contributor)
            elem.append(re_contributors)

        root.append(elem)

    return root
