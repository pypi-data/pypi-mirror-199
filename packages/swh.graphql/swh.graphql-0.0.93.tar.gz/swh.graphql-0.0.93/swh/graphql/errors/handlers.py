# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from ariadne import format_error as original_format_error
from graphql import GraphQLError
import sentry_sdk
from starlette.requests import Request
from starlette.responses import JSONResponse

from .errors import InvalidInputError, ObjectNotFoundError, PaginationError


def format_error(error: GraphQLError, debug: bool = False):
    """
    Response error formatting
    """
    original_format = original_format_error(error, debug)
    if debug:
        # If debug is enabled, reuse Ariadne's formatting logic with stack trace
        return original_format
    expected_errors = [ObjectNotFoundError, PaginationError, InvalidInputError]
    formatted = error.formatted
    formatted["message"] = error.message
    if type(error.original_error) not in expected_errors:
        # a crash, send to sentry
        sentry_sdk.capture_exception(error)
    # FIXME log the original_format to kibana (with stack trace)
    return formatted


def on_auth_error(request: Request, exc: Exception):
    # this error is raised outside the resolver context
    # using the default error formatter to log in sentry
    wrapped_error = GraphQLError("Authentication error", original_error=exc)
    return JSONResponse({"errors": [format_error(wrapped_error)]}, status_code=401)
