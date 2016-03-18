# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Python compatibility module."""

from __future__ import absolute_import, print_function

# Python 2/3 compatibility
try:
    from urllib import urlencode
    PY3 = False
except ImportError:
    from urllib.parse import urlencode
    PY3 = True


__all__ = ('urlencode', 'b', 'text_type', 'string_types')


if PY3:
    text_type = str
    string_types = str

    def b(s):
        """Convert str to bytes."""
        return s.encode('utf8')
else:
    text_type = unicode
    string_types = basestring

    def b(s):
        """Convert str to str."""
        return s
