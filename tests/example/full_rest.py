import os
from datacite import DataCiteRESTClient, schema45

data = {
    "creators": [
        {"name": "Smith, John"},
    ],
    "titles": [
        {
            "title": "Minimal Test Case",
        }
    ],
    "publisher": {"name": "Invenio Software"},
    "publicationYear": "2015",
    "types": {"resourceType": "Dataset", "resourceTypeGeneral": "Dataset"},
    "schemaVersion": "http://datacite.org/schema/kernel-4",
}

# Validate dictionary
schema45.validator.validate(data)

# Generate DataCite XML from dictionary.
doc = schema45.tostring(data)

print(doc)

# Initialize the REST client.
d = DataCiteRESTClient(
    username="DATACITE.ACCOUNT",
    password="mypassword",
    prefix="10.12345",
    test_mode=True,
)

# Mint a DOI
doi = d.public_doi(data, "http://example.org/test-doi")
print(doi)

# Reserve a draft DOI
doi = d.draft_doi(data)
print(doi)

# Make the DOI public
url = d.update_url(doi, url="http://example.org/test-doi2")
d.show_doi(doi)

# Get the DOI metadata
doc = d.get_metadata(doi)

# Hide the DOI
d.hide_doi(doi)
