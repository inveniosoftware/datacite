# -*- coding: utf-8 -*-
#
# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
# Copyright (C) 2024 Arizona State University.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

from collections import defaultdict

"""Errors for the DataCite API.

MDS error responses will be converted into an exception from this module.
Connection issues raises :py:exc:`datacite.errors.HttpError` while DataCite
MDS error responses raises a subclass of
:py:exc:`datacite.errors.DataCiteError`.
"""


class HttpError(Exception):
    """Exception raised when a connection problem happens."""


class DataCiteError(Exception):
    """Exception raised when the server returns a known HTTP error code.

    Known HTTP error codes include:

    * 204 No Content
    * 400 Bad Request
    * 401 Unauthorized
    * 403 Forbidden
    * 404 Not Found
    * 410 Gone (deleted)
    * 412 Precondition Failed
    * 422 Unprocessable Entity
    """

    status_code = 400

    def __init__(self, *args, status_code=500):
        """Initialize this exception with an http status code error."""
        super().__init__(*args)
        self.status_code = status_code

    @staticmethod
    def factory(status_code, *args):
        """Create exceptions through a Factory based on the HTTP error code."""
        return DataCiteErrorFactory.create(status_code, *args)


class DataCiteServerError(DataCiteError):
    """An internal server error happened on the DataCite end. Try later.

    Base class for all 5XX-related HTTP error codes.
    """


class DataCiteRequestError(DataCiteError):
    """A DataCite request error. You made an invalid request.

    Base class for all 4XX-related HTTP error codes as well as 204.
    """


class DataCiteNoContentError(DataCiteRequestError):
    """DOI is known to MDS, but not resolvable.

    This might be due to handle's latency.
    """


class DataCiteBadRequestError(DataCiteRequestError):
    """Bad request error.

    Bad requests can include e.g. invalid XML, wrong domain, wrong prefix.
    Request body must be exactly two lines: DOI and URL
    One or more of the specified mime-types or urls are invalid (e.g. non
    supported mimetype, not allowed url domain, etc.)
    """


class DataCiteUnauthorizedError(DataCiteRequestError):
    """Bad username or password."""


class DataCiteForbiddenError(DataCiteRequestError):
    """Login problem, dataset belongs to another party or quota exceeded."""


class DataCiteNotFoundError(DataCiteRequestError):
    """DOI does not exist in the database."""


class DataCiteGoneError(DataCiteRequestError):
    """Requested dataset was marked inactive (using DELETE method)."""


class DataCitePreconditionError(DataCiteRequestError):
    """Metadata must be uploaded first."""


class DataCiteUnprocessableEntityError(DataCiteRequestError):
    """Invalid metadata format or content."""


class DataCiteErrorFactory:
    """
    Factory class to create specific DataCiteError instances based on the HTTP status code

    Attributes:
        ERROR_CLASSES (defaultdict): A dictionary mapping HTTP status codes to corresponding DataCiteError classes.
    """

    ERROR_CLASSES = defaultdict(
        lambda status_code: (
            DataCiteServerError if status_code >= 500 else DataCiteRequestError
        ),
        {
            204: DataCiteNoContentError,
            400: DataCiteBadRequestError,
            401: DataCiteUnauthorizedError,
            403: DataCiteForbiddenError,
            404: DataCiteNotFoundError,
            410: DataCiteGoneError,
            412: DataCitePreconditionError,
            422: DataCiteUnprocessableEntityError,
        },
    )

    @staticmethod
    def create(status_code, *args):
        """
        Create a specific DataCiteError instance based on the provided error code.

        Args:
            status_code (int): The HTTP status code representing the error.
            args: Additional arguments to be passed to the DataCiteError constructor.

        Returns:
            DataCiteError: An instance of the appropriate DataCiteError subclass.

        """
        DataCiteErrorClass = DataCiteErrorFactory.ERROR_CLASSES[status_code]
        return DataCiteErrorClass(*args, status_code=status_code)
