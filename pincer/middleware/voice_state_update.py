# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.user.voice_state import VoiceState

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def voice_state_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str, List[VoiceState]]:
    """|coro|
    Middleware for the ``on_voice_state_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the voice state update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.user.voice_state.VoiceState`]
        ``on_voice_state_update`` and a ``VoiceState``
    """  # noqa: E501

    voice_state = VoiceState.from_dict(payload.data)
    guild = self.guilds.get(voice_state.guild_id)

    if guild:
        for index, state in enumerate(guild.voice_states):
            if state.user_id == voice_state.user_id:
                guild.voice_states[index] = voice_state
                break
        else:
            guild.voice_states.append(voice_state)

    return "on_voice_state_update", voice_state


def export():
    return voice_state_update_middleware
