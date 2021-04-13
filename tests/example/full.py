from datacite import DataCiteMDSClient, schema42

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

# Initialize the MDS client.
d = DataCiteMDSClient(
    username='MYDC.MYACCOUNT',
    password='mypassword',
    prefix='10.1234',
    test_mode=True,
)

# Set metadata for DOI
d.metadata_post(doc)

# Mint new DOI
d.doi_post('10.1234/test-doi', 'http://example.org/test-doi')

# Get DOI location
location = d.doi_get("10.1234/test-doi")

# Set alternate URL for content type (available through content negotiation)
d.media_post(
    "10.1234/test-doi",
    {"application/json": "http://example.org/test-doi/json/",
     "application/xml": "http://example.org/test-doi/xml/"}
)

# Get alternate URLs
mapping = d.media_get("10.1234/test-doi")
assert mapping["application/json"] == "http://example.org/test-doi/json/"

# Get metadata for DOI
doc = d.metadata_get("10.1234/test-doi")

# Make DOI inactive
d.metadata_delete("10.1234/test-doi")
