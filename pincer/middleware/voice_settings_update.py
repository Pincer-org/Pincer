# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client's voice settings update"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.voice_settings import VoiceSettingsUpdateEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def voice_settings_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_voice_settings_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the voice settings update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.VoiceSettingsUpdateEvent`]
        ``on_voice_settings_update`` and a ``VoiceSettingsUpdateEvent``
    """  # noqa: E501
    return (
        "on_voice_settings_update",
        VoiceSettingsUpdateEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return voice_settings_update_middleware
