# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2018 Center for Open Science.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Module for making requests to the DataCite API."""

import ssl

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from .errors import HttpError


class DataCiteRequest(object):
    """Helper class for making requests.

    :param base_url: Base URL for all requests.
    :param username: HTTP Basic Authentication Username
    :param password: HTTP Basic Authentication Password
    :param default_params: A key/value-mapping which will be converted into a
        query string on all requests.
    :param timeout: Connect and read timeout in seconds. Specify a tuple
        (connect, read) to specify each timeout individually.
    """

    def __init__(self, base_url=None, username=None, password=None,
                 default_params=None, timeout=None):
        """Initialize request object."""
        self.base_url = base_url
        self.username = username
        self.password = password.encode('utf8')
        self.default_params = default_params or {}
        self.timeout = timeout

    def request(self, url, method='GET', body=None, params=None, headers=None):
        """Make a request.

        If the request was successful (i.e no exceptions), you can find the
        HTTP response code in self.code and the response body in self.value.

        :param url: Request URL (relative to base_url if set)
        :param method: Request method (GET, POST, DELETE) supported
        :param body: Request body
        :param params: Request parameters
        :param headers: Request headers
        """
        params = params or {}
        headers = headers or {}

        self.data = None
        self.code = None

        if self.default_params:
            params.update(self.default_params)

        if self.base_url:
            url = self.base_url + url

        if body and isinstance(body, str):
            body = body.encode('utf-8')

        request_func = getattr(requests, method.lower())
        kwargs = dict(
            auth=HTTPBasicAuth(self.username, self.password),
            params=params,
            headers=headers,
        )

        if method == 'POST':
            kwargs['data'] = body
        if method == 'PUT':
            kwargs['data'] = body
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        try:
            return request_func(url, **kwargs)
        except RequestException as e:
            raise HttpError(e)
        except ssl.SSLError as e:
            raise HttpError(e)

    def get(self, url, params=None, headers=None):
        """Make a GET request."""
        return self.request(url, params=params, headers=headers)

    def post(self, url, body=None, params=None, headers=None):
        """Make a POST request."""
        return self.request(url, method="POST", body=body, params=params,
                            headers=headers)

    def put(self, url, body=None, params=None, headers=None):
        """Make a PUT request."""
        return self.request(url, method="PUT", body=body, params=params,
                            headers=headers)

    def delete(self, url, params=None, headers=None):
        """Make a DELETE request."""
        return self.request(url, method="DELETE", params=params,
                            headers=headers)
