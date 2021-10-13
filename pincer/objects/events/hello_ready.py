# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..user.user import User
    from ..guild.guild import Guild
    from ..app.application import Application


@dataclass
class HelloEvent(APIObject):
    """Sent on connection to the websocket.
    Defines the heartbeat interval that the client should heartbeat to.

    Attributes
    ----------
    heartbeat_interval: :class:`int`
        The interval (in milliseconds) the client should heartbeat with
    """
    heartbeat_interval: int


@dataclass
class ReadyEvent(APIObject):
    """Dispatched when a client has completed the initial
    handshake with the gateway (for new sessions).

    Attributes
    ----------
    v: :class:`int`
        Gateway version
    user: :class:`~pincer.objects.user.user.User`
        Information about the user including email
    guilds: List[:class:`~pincer.objects.guild.guild.Guild`]
        The guilds the user is in
    session_id: :class:`str`
        Used for resuming connections
    application: :class:`~pincer.objects.app.application.Application`
        Contains ``id`` and ``flags``
    shard: APINullable[Tuple[:class:`int`, :class:`int`]]
        The shard information associated
        with this session, if sent when identifying
    """
    v: int
    user: User
    guilds: List[Guild]
    session_id: str
    application: Application

    shard: APINullable[Tuple[int, int]] = MISSING
