from typing import Optional


class InvalidTokenError(ValueError):

    def __init__(self, hint: Optional[str] = None):
        """Exception raised when the authorization token is invalid.

        :param hint:
            Additional information about the exception cause.
        """
        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token." + (str(hint) * bool(hint))
        )
