# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user joins a subscribed voice channel"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.user import VoiceState
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def voice_state_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_voice_state_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the voice state create event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.user.voice_state.VoiceState`]
        ``on_voice_state_create`` and a ``VoiceState``
    """
    return (
        "on_voice_state_create",
        VoiceState.from_dict(payload.data),
    )


def export() -> Coro:
    return voice_state_create_middleware
