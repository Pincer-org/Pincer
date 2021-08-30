from typing import Optional


class PincerError(Exception):
    """Base exception class for all Pincer errors."""


class UnhandledException(PincerError):
    def __init__(self, specific: str):
        """
        Exception which gets thrown if an exception wasn't handled.

        If this exception gets thrown please create an issue on our github.
        """
        super(UnhandledException, self).__init__(
            specific + " Please report this to the library devs."
        )


class InvalidTokenError(PincerError, ValueError):
    def __init__(self, hint: Optional[str] = None):
        """
        Exception raised when the authorization token is invalid.

        :param hint:
            Additional information about the exception cause.
        """
        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token." + (str(hint) * bool(hint))
        )


# Discord HTTP Errors
# https://discord.com/developers/docs/topics/opcodes-and-status-codes#http

class HTTPError(PincerError):
    """HTTP Exception base class."""


class NotModifiedError(HTTPError):
    """Error code 304"""


class BadRequestError(HTTPError):
    """Error code 400"""


class UnauthorizedError(HTTPError):
    """Error code 401"""


class ForbiddenError(HTTPError):
    """Error code 403"""


class NotFoundError(HTTPError):
    """Error code 404"""


class MethodNotAllowedError(HTTPError):
    """Error code 405"""


class RateLimitError(HTTPError):
    """Error code 429"""


class GatewayError(HTTPError):
    """Error code 502"""


class ServerError(HTTPError):
    """
    Error code 5xx
    Status code is not in the discord API
    """
