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
d = DataCiteRESTClient(
    username="MYDC.MYACCOUNT",
    password="mypassword",
    prefix="10.1234",
    test_mode=True
)

# Reserve a draft DOI
doi = d.draft_doi()
