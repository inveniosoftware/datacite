# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015, 2016 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.


"""Python API wrapper for the DataCite API."""

from .client import DataCiteMDSClient
from .rest_client import DataCiteRESTClient

__version__ = "1.3.0"

__all__ = ("DataCiteMDSClient", "DataCiteRESTClient", "__version__")
