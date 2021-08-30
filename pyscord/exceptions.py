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
