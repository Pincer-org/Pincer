# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake


@dataclass
class VoiceServerUpdateEvent(APIObject):
    """
    Sent when a guild's voice server is updated.
    This is sent when initially connecting to voice,
    and when the current voice instance fails over to a new server.

    :param token:
        voice connection token

    :param guild_id:
        the guild this voice server update is for

    :param endpoint:
        the voice server host
    """

    token: str
    guild_id: Snowflake
    endpoint: Optional[str] = None


@dataclass
class VoiceChannelSelectEvent(APIObject):
    """
    Sent when the client joins a voice channel

    :param channel_id:
        id of channel

    :param guild_id:
        id of guild
    """

    channel_id: Optional[Snowflake] = None
    guild_id: Optional[Snowflake] = None


class VoiceConnectionStates(Enum):
    """
    :param DISCONNECTED:
        TCP disconnected

    :param AWAITING_ENDPOINT:
        Waiting for voice endpoint

    :param AUTHENTICATING:
        TCP authenticating

    :param CONNECTING:
        TCP connecting

    :param CONNECTED:
        TCP connected

    :param VOICE_DISCONNECTED:
        TCP connected, Voice disconnected

    :param VOICE_CONNECTING:
        TCP connected, Voice connecting

    :param VOICE_CONNECTED:
        TCP connected, Voice connected

    :param NO_ROUTE:
        No route to host

    :param ICE_CHECKING:
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
    
    :param state:
        one of the voice connection states listed below

    :param hostname:
        hostname of the connected voice server

    :param pings:
        last 20 pings (in ms)

    :param average_ping:
        average ping (in ms)

    :param last_ping:
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

    :param user_id:
        id of user who started speaking
    """

    user_id: Snowflake


@dataclass
class SpeakingStopEvent(APIObject):
    """
    Sent when a user in a subscribed voice channel stops speaking

    :param user_id:
        id of user who stopped speaking
    """

    user_id: Snowflake
