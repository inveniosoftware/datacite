from datacite import DataCiteMDSClient, schema40

# If you want to generate XML for earlier version 3.1, you need to use
# schema31 instead.

data = {
    'identifier': {
        'identifier': '10.5072/test-doi',
        'identifierType': 'DOI',
    },
    'creators': [
        {'creatorName': 'Smith, John'}
    ],
    'titles': [
        {'title': 'DataCite PyPI Package'}
    ],
    'publisher': 'CERN',
    'publicationYear': '2015',
    'resourceType': {
        'resourceTypeGeneral': 'Dataset'
    }
}

# Validate dictionary
assert schema40.validate(data)

# Generate DataCite XML from dictionary.
doc = schema40.tostring(data)

# Initialize the MDS client.
d = DataCiteMDSClient(
    username='MYDC.MYACCOUNT',
    password='mypassword',
    prefix='10.5072',
    test_mode=True
)

# Set metadata for DOI
d.metadata_post(doc)

# Mint new DOI
d.doi_post('10.5072/test-doi', 'http://example.org/test-doi')

# Get DOI location
location = d.doi_get("10.5072/test-doi")

# Set alternate URL for content type (availble through content negotiation)
d.media_post(
    "10.5072/test-doi",
    {"application/json": "http://example.org/test-doi/json/",
     "application/xml": "http://example.org/test-doi/xml/"}
)

# Get alternate URLs
mapping = d.media_get("10.5072/test-doi")
assert mapping["application/json"] == "http://example.org/test-doi/json/"

# Get metadata for DOI
doc = d.metadata_get("10.5072/test-doi")

# Make DOI inactive
d.metadata_delete("10.5072/test-doi")
