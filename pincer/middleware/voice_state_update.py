# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..core.dispatch import GatewayDispatch
    from ..objects.user.voice_state import VoiceState


async def voice_state_update_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[VoiceState]]:
    """|coro|

    Middleware for ``on_voice_state_update`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.user.voice_state.VoiceState`]]
        ``on_voice_state_update`` and a ``VoiceState``
    """
    return "on_voice_state_update", [
        VoiceState.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]


def export():
    return voice_state_update_middleware
