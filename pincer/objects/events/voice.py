# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Optional, List

    from ...utils.snowflake import Snowflake


@dataclass
class VoiceServerUpdateEvent(APIObject):
    """Sent when a guild's voice server is updated.
    This is sent when initially connecting to voice,
    and when the current voice instance fails over to a new server.

    Attributes
    ----------
    token: :class:`str`
        Voice connection token
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The guild this voice server update is for
    endpoint: Optional[:class:`str`]
        The voice server host
    """

    token: str
    guild_id: Snowflake
    endpoint: Optional[str] = None


@dataclass
class VoiceChannelSelectEvent(APIObject):
    """
    Sent when the client joins a voice channel

    Attributes
    ----------
    channel_id : Optional[:class:`Snowflake`]
        id of channel

    guild_id : Optional[:class:`Snowflake`]
        id of guild
    """

    channel_id: Optional[Snowflake] = None
    guild_id: Optional[Snowflake] = None


class VoiceConnectionStates(Enum):
    """
    Attributes
    ----------
    DISCONNECTED : :class:`str`
        TCP disconnected

    AWAITING_ENDPOINT : :class:`str`
        Waiting for voice endpoint

    AUTHENTICATING : :class:`str`
        TCP authenticating

    CONNECTING : :class:`str`
        TCP connecting

    CONNECTED : :class:`str`
        TCP connected

    VOICE_DISCONNECTED : :class:`str`
        TCP connected, Voice disconnected

    VOICE_CONNECTING : :class:`str`
        TCP connected, Voice connecting

    VOICE_CONNECTED : :class:`str`
        TCP connected, Voice connected

    NO_ROUTE : :class:`str`
        No route to host

    ICE_CHECKING : :class:`str`
        WebRTC ice checking

    """

    DISCONNECTED = auto()
    AWAITING_ENDPOINT = auto()
    AUTHENTICATING = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    VOICE_DISCONNECTED = auto()
    VOICE_CONNECTING = auto()
    VOICE_CONNECTED = auto()
    NO_ROUTE = auto()
    ICE_CHECKING = auto()


@dataclass
class VoiceConnectionStatusEvent(APIObject):
    """
    Sent when the client's voice connection status changes

    state : :class:`VoiceConnectionStates`
        one of the voice connection states listed below

    hostname : :class:`str`
        hostname of the connected voice server

    pings : List[:class:`int`]
        last 20 pings (in ms)

    average_ping : :class:`int`
        average ping (in ms)

    last_ping : :class:`int`
        last ping (in ms)

    """

    state: VoiceConnectionStates
    hostname: str
    pings: List[int]
    average_ping: int
    last_ping: int


@dataclass
class SpeakingStartEvent(APIObject):
    """
    Sent when a user in a subscribed voice channel speaks

    Attributes
    ----------
    user_id : :class:`Snowflake`
        id of user who started speaking
    """

    user_id: Snowflake


@dataclass
class SpeakingStopEvent(APIObject):
    """
    Sent when a user in a subscribed voice channel stops speaking

    Attributes
    ----------
    user_id : :class:`Snowflake`
        id of user who stopped speaking
    """

    user_id: Snowflake
