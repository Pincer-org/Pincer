# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..utils.api_object import APIObject

if TYPE_CHECKING:
    from .emoji import Emoji


@dataclass
class Reaction(APIObject):
    """
    Represents a Discord Reaction object

    :param count:
        times this emoji has been used to react

    :param me:
        whether the current user reacted using this emoji

    :param emoji:
        emoji information
    """
    count: int
    me: bool
    emoji: Emoji
