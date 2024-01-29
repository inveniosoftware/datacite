# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Python API client wrapper for the DataCite Metadata Store API.

API documentation is available at
https://support.datacite.org/docs/mds-api-guide.
"""

import requests

from .errors import DataCiteError
from .request import DataCiteRequest

HTTP_OK = requests.codes["ok"]
HTTP_CREATED = requests.codes["created"]


class DataCiteMDSClient(object):
    """DataCite MDS API client wrapper.

    Warning: The DataCite MDS API is being maintained but is no longer actively
    developed.
    """

    def __init__(
        self, username, password, prefix, test_mode=False, url=None, timeout=None
    ):
        """Initialize the API client wrapper.

        :param username: DataCite username.
        :param password: DataCite password.
        :param prefix: DOI prefix (or CFG_DATACITE_DOI_PREFIX).
        :param test_mode: use test URL when True
        :param url: DataCite API base URL.
        :param timeout: Connect and read timeout in seconds. Specify a tuple
            (connect, read) to specify each timeout individually.
        """
        self.username = username
        self.password = password
        self.prefix = prefix

        if test_mode:
            self.api_url = "https://mds.test.datacite.org/"
        else:
            self.api_url = url or "https://mds.datacite.org/"

        if not self.api_url.endswith("/"):
            self.api_url += "/"

        self.timeout = timeout

    def __repr__(self):
        """Create string representation of object."""
        return "<DataCiteMDSClient: {0}>".format(self.username)

    def _create_request(self):
        """Create a new Request object."""
        return DataCiteRequest(
            base_url=self.api_url,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
        )

    def doi_get(self, doi):
        """Get the URL where the resource pointed by the DOI is located.

        :param doi: DOI name of the resource.
        """
        request = self._create_request()
        resp = request.get("doi/" + doi)
        if resp.status_code == HTTP_OK:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def doi_post(self, new_doi, location):
        """Mint new DOI.

        :param new_doi: DOI name for the new resource.
        :param location: URL where the resource is located.
        :return: "CREATED" or "HANDLE_ALREADY_EXISTS".
        """
        headers = {"Content-Type": "text/plain;charset=UTF-8"}
        # Use \r\n for HTTP client data.
        body = "\r\n".join(["doi=%s" % new_doi, "url=%s" % location])

        request = self._create_request()
        resp = request.post("doi", body=body, headers=headers)

        if resp.status_code == HTTP_CREATED:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def metadata_get(self, doi):
        """Get the XML metadata associated to a DOI name.

        :param doi: DOI name of the resource.
        """
        headers = {"Accept": "application/xml", "Accept-Encoding": "UTF-8"}

        request = self._create_request()
        resp = request.get("metadata/" + doi, headers=headers)

        if resp.status_code == HTTP_OK:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def metadata_post(self, metadata):
        """Set new metadata for an existing DOI.

        Metadata should follow the DataCite Metadata Schema:
        http://schema.datacite.org/

        :param metadata: XML format of the metadata.
        :return: "CREATED" or "HANDLE_ALREADY_EXISTS"
        """
        headers = {
            "Content-Type": "application/xml;charset=UTF-8",
        }

        request = self._create_request()
        resp = request.post("metadata", body=metadata, headers=headers)

        if resp.status_code == HTTP_CREATED:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def metadata_delete(self, doi):
        """Mark as 'inactive' the metadata set of a DOI resource.

        :param doi: DOI name of the resource.
        :return: "OK"
        """
        request = self._create_request()
        resp = request.delete("metadata/" + doi)

        if resp.status_code == HTTP_OK:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def media_get(self, doi):
        """Get list of pairs of media type and URLs associated with a DOI.

        :param doi: DOI name of the resource.
        """
        request = self._create_request()
        resp = request.get("media/" + doi)

        if resp.status_code == HTTP_OK:
            values = {}
            for line in resp.text.splitlines():
                mimetype, url = line.split("=", 1)
                values[mimetype] = url
            return values
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)

    def media_post(self, doi, media):
        """Add/update media type/urls pairs to a DOI.

        Standard domain restrictions check will be performed.

        :param media: Dictionary of (mime-type, URL) key/value pairs.
        :return: "OK"
        """
        headers = {"Content-Type": "text/plain;charset=UTF-8"}

        # Use \r\n for HTTP client data.
        body = "\r\n".join(["%s=%s" % (k, v) for k, v in media.items()])

        request = self._create_request()
        resp = request.post("media/" + doi, body=body, headers=headers)

        if resp.status_code == HTTP_OK:
            return resp.text
        else:
            raise DataCiteError.factory(resp.status_code, resp.text)
