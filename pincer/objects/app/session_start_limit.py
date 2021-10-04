# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject


@dataclass
class SessionStartLimit(APIObject):
    """
    Represents a Discord Session Start Limit object

    :param total:
        The total number of session starts the current user is allowed

    :param remaining:
        The remaining number of session starts
        the current user is allowed

    :param reset_after:
        The number of milliseconds after which the limit resets

    :param max_concurrency:
        The number of identify requests allowed per 5 seconds
    """
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int
