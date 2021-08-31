# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Optional


class PincerError(Exception):
    """Base exception class for all Pincer errors."""


class UnhandledException(PincerError):
    def __init__(self, specific: str):
        """
        Exception which gets thrown if an exception wasn't handled.

        Please create an issue on our github
        if this exception gets thrown.
        """
        super(UnhandledException, self).__init__(
            specific + " Please report this to the library devs."
        )


class DispatchError(PincerError):
    """
    Base exception class for all errors which are specifically related
    to the dispatcher.
    """


class InvalidTokenError(DispatchError, ValueError):
    def __init__(self, hint: Optional[str] = None):
        """
        Exception raised when the authorization token is invalid.

        :param hint:
            Additional information about the exception cause.
        """
        if hint is None:
            hint = ''

        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token.\n" + hint
        )


class HeartbeatError(DispatchError):
    """Exception raised due to a problem with websocket heartbeat."""


# Discord HTTP Errors
# `developers/docs/topics/opcodes-and-status-codes#http`

class HTTPError(PincerError):
    """HTTP Exception base class."""


class NotModifiedError(HTTPError):
    """Error code 304."""


class BadRequestError(HTTPError):
    """Error code 400."""


class UnauthorizedError(HTTPError):
    """Error code 401."""


class ForbiddenError(HTTPError):
    """Error code 403."""


class NotFoundError(HTTPError):
    """Error code 404."""


class MethodNotAllowedError(HTTPError):
    """Error code 405."""


class RateLimitError(HTTPError):
    """Error code 429."""


class GatewayError(HTTPError):
    """Error code 502."""


class ServerError(HTTPError):
    """
    Error code 5xx.
    Status code is not in the discord API
    """
