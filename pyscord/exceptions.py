from typing import Optional


class PyscordError(Exception):
    """
    Base exception class for all Pyscord errors.
    """
    pass


class UnhandledException(PyscordError):
    def __init__(self, specific: str):
        """
        Exception which gets thrown if an exception wasn't handled.

        If this exception gets thrown please create an issue on our github.
        """
        super(UnhandledException, self).__init__(
            specific + " Please report this to the library devs."
        )


class InvalidTokenError(PyscordError, ValueError):
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

class NotModifiedError(PyscordError):
    """Error code 304"""

class BadRequestError(PyscordError):
    """Error code 400"""

class UnauthorizedError(PyscordError):
    """Error code 401"""

class ForbiddenError(PyscordError):
    """Error code 403"""

class NotFoundError(PyscordError):
    """Error code 404"""

class MethodNotAllowedError(PyscordError):
    """Error code 405"""

class RateLimitError(PyscordError):
    """Error code 429"""

class GatewayError(PyscordError):
    """Error code 502"""

class ServerError(PyscordError):
    """
    Error code 5xx
    Status code is not in the discord API
    """
