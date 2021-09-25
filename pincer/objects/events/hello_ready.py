# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import List, Tuple

from ...objects.application import Application
from ...objects.guild import Guild
from ...objects.user import User
from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable


@dataclass
class HelloEvent(APIObject):
    """
    Sent on connection to the websocket.
    Defines the heartbeat interval that the client should heartbeat to.

    :param heartbeat_interval:
        the interval (in milliseconds) the client should heartbeat with
    """
    heartbeat_interval: int


@dataclass
class ReadyEvent(APIObject):
    """
    Dispatched when a client has completed the initial
    handshake with the gateway (for new sessions).

    :param v:
        gateway version

    :param user:
        information about the user including email

    :param guilds:
        the guilds the user is in

    :param session_id:
        used for resuming connections

    :param shard:
        the shard information associated
        with this session, if sent when identifying

    :param application:
        contains `id` and `flags`
    """
    v: int
    user: User
    guilds: List[Guild]
    session_id: str
    application: Application

    shard: APINullable[Tuple[int, int]] = MISSING
