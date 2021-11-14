# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from ..guild.member import GuildMember
    from ...utils.snowflake import Snowflake


@dataclass
class TypingStartEvent(APIObject):
    """Sent when a user starts typing in a channel.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the channel
    user_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the user
    timestamp: :class:`int`
        Unix time (in seconds) of when the user started typing
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the guild
    member: APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
        The member who started typing if this happened in a guild
    """
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
