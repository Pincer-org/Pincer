# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client's voice connection status changes"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.voice import VoiceConnectionStatusEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def voice_connection_status_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_voice_connection_status`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the voice connection status event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.voice.VoiceConnectionStatusEvent`]
        ``on_voice_connection_status`` and a ``VoiceConnectionStatusEvent``
    """  # noqa: E501
    return (
        "on_voice_connection_status",
        VoiceConnectionStatusEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return voice_connection_status_middleware
