from typing import Optional


class InvalidTokenError(ValueError):

    def __init__(self, hint: Optional[str] = None):
        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token." + (hint * bool(hint))
        )
