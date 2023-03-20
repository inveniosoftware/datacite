Changes
=======

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
