from datacite import DataCiteMDSClient

# Create a DataCite XML document.
doc = '''<resource
  xmlns="http://datacite.org/schema/kernel-3"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://datacite.org/schema/kernel-3
  http://schema.datacite.org/meta/kernel-3/metadata.xsd">
    <identifier identifierType="DOI">10.5072/test-doi</identifier>
    <creators>
        <creator>
            <creatorName>Smith, John</creatorName>
        </creator>
    </creators>
    <titles>
        <title>DataCite PyPI Package</title>
    </titles>
    <publisher>CERN</publisher>
    <publicationYear>2015</publicationYear>
</resource>
'''

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
