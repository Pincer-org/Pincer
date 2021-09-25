# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from .guild_member import GuildMember
from ..utils import APIObject, APINullable, MISSING, Snowflake, Timestamp


@dataclass
class VoiceState(APIObject):
    """
    Used to represent a user's voice connection status

    :param guild_id:
        the guild id this voice state is for

    :param channel_id:
        the channel id this user is connected to

    :param user_id:
        the user id this voice state is for

    :param member:
        the guild member this voice state is for

    :param session_id:
        the session id for this voice state

    :param deaf:
        whether this user is deafened by the server

    :param mute:
        whether this user is muted by the server

    :param self_deaf:
        whether this user is locally deafened

    :param self_mute:
        whether this user is locally muted

    :param self_stream:
        whether this user is streaming using "Go Live"

    :param self_video:
        whether this user's camera is enabled

    :param suppress:
        whether this user is muted by the current user

    :param request_to_speak_timestamp:
        the time at which the user requested to speak
    """
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
