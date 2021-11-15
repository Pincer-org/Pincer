# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


@dataclass
class ChannelPinsUpdateEvent(APIObject):
    """Sent when a message is pinned or unpinned in a text channel.
    This is not sent when a pinned message is deleted.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    last_pin_timestamp: APINullable[:class:`~pincer.utils.timestamp.Timestamp`]
        The time at which the most recent pinned message was pinned
    """
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING
    last_pin_timestamp: APINullable[Timestamp] = MISSING

