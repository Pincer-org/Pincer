# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client joins a voice channel"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.voice import VoiceChannelSelectEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def voice_channel_select_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_voice_channel_select`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the voice channel select event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.voice.VoiceChannelSelectEvent`]
        ``on_voice_channel_select`` and a ``VoiceChannelSelectEvent``
    """  # noqa: E501
    return (
        "on_voice_channel_select",
        VoiceChannelSelectEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return voice_channel_select_middleware
