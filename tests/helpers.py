# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test helpers."""

from __future__ import absolute_import, unicode_literals, print_function

import functools
import sys

from datacite import DataCiteMDSClient

APIURL = "https://mds.example.org/"
PY34 = sys.hexversion >= 0x03040000


def import_httpretty():
    """Import HTTPretty and monkey patch Python 3.4 issue.

    See https://github.com/gabrielfalcao/HTTPretty/pull/193 and
    as well as https://github.com/gabrielfalcao/HTTPretty/issues/221.
    """
    if not PY34:
        import httpretty
    else:
        import socket
        old_SocketType = socket.SocketType

        import httpretty
        from httpretty import core

        def sockettype_patch(f):
            @functools.wraps(f)
            def inner(*args, **kwargs):
                f(*args, **kwargs)
                socket.SocketType = old_SocketType
                socket.__dict__['SocketType'] = old_SocketType
            return inner

        core.httpretty.disable = sockettype_patch(
            httpretty.httpretty.disable
        )
    return httpretty


def get_client(username="DC", password="pw", prefix='10.5072',
               test_mode=False, timeout=None):
    """Create a API client."""
    return DataCiteMDSClient(
        username=username,
        password=password,
        prefix=prefix,
        url=APIURL,
        test_mode=test_mode,
        timeout=timeout,
    )
