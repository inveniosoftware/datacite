Changes
=======

Version v1.3.0 (released 2025-07-03):

- Removes deprecated schema 3.1
- Adds minimum python version 3.9
- Switches 4.5 schema to https
- Documentation clanup and improvements

Version v1.2.0 (released 2024-10-17):

- Updates package setup and adds black formatting
- Adds support for DataCite Metadata Schema v4.5.
  The version 4.5 jsonschema includes a number of 
  changes and improvements:

  - Switches to jsonschema 2019-09 and adds more complete validation
    to catch mistyped elements
  - Switches publisher from a string to an object. This means
    you will need to change publisher to be structured like 
    `"publisher": {"name": "Invenio Software"}` 
    when you use version 4.5. This change is needed to
    support the addition of publisher identifiers.
  - Removes the identifiers field and added doi, prefix, and suffix fields.
    These fields are clearer, and DataCite appears to be moving away from the
    combined identifiers field. doi is not a required field since you may or
    may not have a DOI depending on your workflow.
  - Adds new relatedItem elements for publication metadata
  - Switches geolocation point values to numbers. This is to enable 
    validation and is consistent with GeoJson and InvenioRDM. It is 
    different from the DataCite REST API which uses strings, and
    submitted numbers will be turned into strings by DataCite.
  - Reorganizes geolocationPolygon to how DataCite is currently rendering this
    metadata
  - Adds support for the new resourceTypeGeneral and relationType values
  - General jsonschema organization improvements

Version v1.1.3 (released 2023-03-20):

- Updates dependency versions and adds python 3.9 support
- Changes internal definition name for affiliation in 4.3 schema

Version v1.1.2 (released 2021-06-22):

- Standardizes function names in DataCiteRESTClient. Old functions will be
  depreciated in a future release

Version v1.1.1 (released 2021-04-20):

- Fixes DataCiteRESTClient attributes' type. Prefix, username and password
  are always cast to string.

Version v1.1.0 (released 2021-04-15):

- Adds full support for DataCite Metadata Schema v4.2 and v4.3 XML generation.
- Uses Official DataCite JSON Schema, which has the following notable changes
  from the previous schema:

  - Uses "identifiers" which is a combination of the XML "identifier" and
    "alternativeIdentifiers" elements
  - "creatorName" is now "name"
  - "contributorName" is now "name"
  - "affiliations" is now "affiliation" (is still an array)
  - "affilition" is now "name"
  - There is no longer a funder identifier object (the identifier and type are just
    elements)
- Removes Python 2 support
- Removes the old way of testing with DataCite: test mode for the MDS APIs and
  the test DOI 10.5072

Version v1.0.1 (released 2018-03-08):

- Fixes schema location url for DataCite v4.1

Version v1.0.0 (released 2018-02-28):

- Adds full support for DataCite Metadata Schema v4.1 XML generation.

Version v0.3.0 (released 2016-11-18):

- Adds full support for DataCite Metadata Schema v4.0 XML generation.

- Adds the message from the server in the error exceptions.

Version v0.2.2 (released 2016-09-23):

- Fixes issue with generated order of nameIdentifier and affiliation tags.

Version v0.2.1 (released 2016-03-29):

- Fixes issue with JSON schemas not being included when installing from PyPI.

Version v0.2.0 (released 2016-03-21):

- Adds DataCite XML generation support.

Version 0.1 (released 2015-02-25):

- Initial public release.
