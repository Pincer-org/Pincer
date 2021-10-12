# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from ..guild.member import GuildMember
    from ...utils.snowflake import Snowflake


@dataclass
class TypingStartEvent(APIObject):
    """
    Sent when a user starts typing in a channel.

    :param channel_id:
        id of the channel

    :param guild_id:
        id of the guild

    :param user_id:
        id of the user

    :param timestamp:
        unix time (in seconds) of when the user started typing

    :param member:
        the member who started typing if this happened in a guild
    """
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
