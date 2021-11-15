# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


class PrivacyLevel(IntEnum):
    """Represents the level of publicity of a stage.

    Attributes
    ----------
    PUBLIC:
        The stage is public.
    GUILD_ONLY:
        The stage of for guild members only.
    """
    PUBLIC = 1
    GUILD_ONLY = 2


@dataclass
class StageInstance(APIObject):
    """Represents a Stage Instance object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of this Stage instance
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Guild id of the associated Stage channel
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the associated Stage channel
    topic: :class:`str`
        Topic of the Stage instance (1-120 characters)
    privacy_level: :class:`~pincer.objects.guild.stage.PrivacyLevel`
        Privacy level of the Stage instance
    discoverable: :class:`bool`
        Is Stage Discovery enabled
    """
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable: bool
