# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from pincer.utils.api_object import APIObject
from pincer.utils.snowflake import Snowflake
from pincer.utils.timestamp import Timestamp
from pincer.utils.types import MISSING, APINullable


@dataclass
class ChannelPinsUpdateEvent(APIObject):
    """
    Sent when a message is pinned or unpinned in a text channel.
    This is not sent when a pinned message is deleted.

    :param guild_id:
        the id of the guild

    :param channel_id:
        the id of the channel

    :param last_pin_timestamp:
        the time at which the most recent pinned message was pinned
    """
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING
    last_pin_timestamp: APINullable[Timestamp] = MISSING
