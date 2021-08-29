class InvalidTokenError(ValueError):

    def __init__(self):
        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token."
        )
