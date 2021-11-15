# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Optional

    from ..guild.member import GuildMember
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


@dataclass
class VoiceState(APIObject):
    """Used to represent a user's voice connection status

    Attributes
    ----------
    channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The channel id this user is connected to
    user_id: :class:`~pincer.utils.snowflake.Snowflake`
        The user id this voice state is for
    session_id: :class:`str`
        The session id for this voice state
    deaf: :class:`bool`
        Whether this user is deafened by the server
    mute: :class:`bool`
        Whether this user is muted by the server
    self_deaf: :class:`bool`
        Whether this user is locally deafened
    self_mute: :class:`bool`
        Whether this user is locally muted
    self_video: :class:`bool`
        Whether this user's camera is enabled
    suppress: :class:`bool`
        Whether this user is muted by the current user
    request_to_speak_timestamp: Optional[:class:`~pincer.utils.timestamp.Timestamp`]
        The time at which the user requested to speak
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The guild id this voice state is for
    member: APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
        The guild member this voice state is for
    self_stream: APINullable[:class:`bool`]
        Whether this user is streaming using "Go Live"
    """
    # noqa: E501

    channel_id: Optional[Snowflake]
    user_id: Snowflake
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: Optional[Timestamp]

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
    self_stream: APINullable[bool] = MISSING
