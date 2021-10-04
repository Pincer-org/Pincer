# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...exceptions import PincerError
from ...utils import APIObject


@dataclass
class DiscordError(PincerError, APIObject):
    """
    Represents an error event in the Discord Gateway.

    :param code:
        The RPC error code.

    :param message:
        The error description..
    """
    code: int
    message: str
