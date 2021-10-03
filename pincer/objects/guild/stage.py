# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils import APIObject

if TYPE_CHECKING:
    from ...utils import Snowflake


class PrivacyLevel(IntEnum):
    """
    Represents the level of publicity of a stage.
    """
    PUBLIC = 1
    GUILD_ONLY = 2


@dataclass
class StageInstance(APIObject):
    """
    Represents a Stage Instance object

    :param id:
        id of this Stage instance

    :param guild_id:
        guild id of the associated Stage channel

    :param channel_id:
        id of the associated Stage channel

    :param topic:
        topic of the Stage instance (1-120 characters)

    :param privacy_level:
        privacy level of the Stage instance

    :param discoverable:
        is Stage Discovery enabled
    """
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable: bool

    @property
    def discoverable_disabled(self) -> bool:
        return not self.discoverable
