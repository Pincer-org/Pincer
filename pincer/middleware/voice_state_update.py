# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""

from ..core.dispatch import GatewayDispatch
from ..objects.user import VoiceState
from ..utils.conversion import construct_client_dict


async def voice_state_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_voice_state_update`` event.

    Parameters
    ----------
    :param self:
        The current client.

    :param payload:
        The data received from the voice state update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.user.voice_state.VoiceState`]]
        ``on_voice_state_update`` and a ``VoiceState``
    """
    return "on_voice_state_update", [
        VoiceState.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return voice_state_update_middleware
