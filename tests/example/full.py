from datacite import DataCiteMDSClient, schema46

prefix = "10.1234"

data = {
    "doi": f"{prefix}/test-doi",
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
assert schema46.validate(data)

# Generate DataCite XML from dictionary.
doc = schema46.tostring(data)

# Initialize the MDS client.
d = DataCiteMDSClient(
    username="DATACITE.ACCOUNT",
    password="mypassword",
    prefix=prefix,
    test_mode=True,
)

# Set metadata for DOI
d.metadata_post(doc)

# Mint new DOI
d.doi_post(f"{prefix}/test-doi", "http://example.org/test-doi")

# Get DOI location
location = d.doi_get(f"{prefix}/test-doi")

# Set alternate URL for content type (available through content negotiation)
d.media_post(
    f"{prefix}/test-doi",
    {
        "application/json": "http://example.org/test-doi/json/",
        "application/xml": "http://example.org/test-doi/xml/",
    },
)

# Get alternate URLs
mapping = d.media_get(f"{prefix}/test-doi")
assert mapping["application/json"] == "http://example.org/test-doi/json/"

# Get metadata for DOI
doc = d.metadata_get(f"{prefix}/test-doi")

# Make DOI inactive
d.metadata_delete(f"{prefix}/test-doi")
