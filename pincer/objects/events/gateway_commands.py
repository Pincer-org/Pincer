# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import auto, Enum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Union

    from .presence import Activity
    from ..app.intents import Intents
    from ...utils.snowflake import Snowflake


@dataclass
class Identify(APIObject):
    """Used to trigger the initial handshake with the gateway.

    Attributes
    ----------
    token: :class:`str`
        Authentication token
    properties: Dict[:class:`str`, :class:`str`]
        Connection properties
    intents: :class:`~pincer.objects.app.intents.Intents`
        The Gateway Intents you wish to receive
    compress: APINullable[:class:`bool`]
        Whether this connection supports compression of packets
    large_threshold: APINullable[:class:`int`]
        Value between 50 and 250, total number
        of members where the gateway will stop sending offline
        members in the guild member list
    shard: APINullable[Tuple[:class:`int`, :class:`int`]]
        Used for Guild Sharding
    presence: APINullable[Any]
        Presence structure for initial presence information
    """
    token: str
    properties: Dict[str, str]
    intents: Intents

    compress: APINullable[bool] = MISSING
    large_threshold: APINullable[int] = MISSING
    shard: APINullable[Tuple[int, int]] = MISSING
    presence: APINullable[Any] = MISSING  # FIXME


@dataclass
class Resume(APIObject):
    """Used to replay missed events when a disconnected client resumes.

    Attributes
    ----------
    token: :class:`str`
        Session token
    session_id: :class:`str`
        Session id
    seq: :class:`int`
        Last sequence number received
    """
    token: str
    session_id: str
    seq: int


@dataclass
class RequestGuildMembers(APIObject):
    """Used to request all members for a guild or a list of guilds.

    guild_id:
        id of the guild to get members for

    query:
        string that username starts with, or an empty string
        to return all members

    limit:
        maximum number of members to send matching the `query`;
        a limit of `0` can be used with an empty string `query`
        to return all members

    presences:
        used to specify if we want the presences of the matches members

    user_ids:
        used to specify which users you wish to fetch

    nonce:
        nonce to identify the Guild Members Chunk response
    """
    guild_id: Snowflake
    limit: int

    query: APINullable[str] = MISSING
    presences: APINullable[bool] = MISSING
    user_ids: APINullable[Union[Snowflake, List[Snowflake]]] = MISSING
    nonce: APINullable[str] = MISSING


@dataclass
class UpdateVoiceState(APIObject):
    """Sent when a client wants to join, move,
    or disconnect from a voice channel.

    guild_id:
        id of the guild

    channel_id:
        id of the voice channel client
        wants to join (null if disconnecting)

    self_mute:
        is the client muted

    self_deaf:
        is the client deafened
    """
    guild_id: Snowflake
    self_mute: bool
    self_deaf: bool

    channel_id: Optional[Snowflake] = None


class StatusType(Enum):
    """online:
        Online

    dnd:
        Do Not Disturb

    idle:
        AFK

    invisible:
        Invisible and shown as offline

    offline:
        Offline
    """
    online = auto()
    dnd = auto()
    idle = auto()
    invisible = auto()
    offline = auto()


@dataclass
class UpdatePresence(APIObject):
    """Sent by the client to indicate a presence or status update.

    since:
        unix time (in milliseconds) of when the client went idle,
        or null if the client is not idle

    activities:
        the user's activities

    status:
        the user's new status

    afk:
        whether or not the client is afk
    """
    activities: List[Activity]
    status: StatusType
    afk: bool
    since: Optional[int] = None
