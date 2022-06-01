# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject


@dataclass(repr=False)
class SessionStartLimit(APIObject):
    """Represents a Discord Session Start Limit

    Attributes
    ----------
    total: :class:`int`
        The total number of session starts the current user is allowed
    remaining: :class:`int`
        The remaining number of session starts
        the current user is allowed
    reset_after: :class:`int`
        The number of milliseconds after which the limit resets
    max_concurrency: :class:`int`
        The number of identify requests allowed per 5 seconds
    """

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int
