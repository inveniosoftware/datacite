import os
from datacite import DataCiteRESTClient, schema42

# If you want to generate XML for earlier versions, you need to use either the
# schema31, schema40 or schema41 instead.

data = {
    'identifiers': [{
        'identifierType': 'DOI',
        'identifier': '10.1234/foo.bar',
    }],
    'creators': [
        {'name': 'Smith, John'},
    ],
    'titles': [
        {'title': 'Minimal Test Case', }
    ],
    'publisher': 'Invenio Software',
    'publicationYear': '2015',
    'types': {
        'resourceType': 'Dataset',
        'resourceTypeGeneral': 'Dataset'
    },
    'schemaVersion': 'http://datacite.org/schema/kernel-4',
}

# Validate dictionary
assert schema42.validate(data)

# Generate DataCite XML from dictionary.
doc = schema42.tostring(data)

# Initialize the REST client.
username = os.environ["DATACITE_USER"]
password = os.environ["DATACITE_PW"]
prefix = os.environ["DATACITE_PREFIX"]
d = DataCiteRESTClient(
    username=username,
    password=password,
    prefix=prefix,
    test_mode=True
)

# Reserve a draft DOI
doi = d.draft_doi()

# Mint new DOI
#d.doi_post('10.5072/test-doi', 'http://example.org/test-doi')

# Get DOI location
#location = d.doi_get(doi)

# Set alternate URL for content type (available through api)
#d.media_post(
#    "10.5072/test-doi",
#    {"application/json": "http://example.org/test-doi/json/",
#     "application/xml": "http://example.org/test-doi/xml/"}
#)

# Get alternate URLs
#mapping = d.media_get("10.5072/test-doi")
#assert mapping["application/json"] == "http://example.org/test-doi/json/"

# Get metadata for DOI
#doc = d.metadata_get("10.5072/test-doi")

# Make DOI inactive
#d.metadata_delete("10.5072/test-doi")
