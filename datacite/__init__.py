# SPDX-FileCopyrightText: 2015, 2016 CERN.
# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: BSD-3-Clause


"""Python API wrapper for the DataCite API."""

from .client import DataCiteMDSClient
from .rest_client import DataCiteRESTClient

__version__ = "1.4.1"

__all__ = ("DataCiteMDSClient", "DataCiteRESTClient", "__version__")
