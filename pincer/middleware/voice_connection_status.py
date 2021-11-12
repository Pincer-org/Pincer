# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client's voice connection status changes"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.voice import VoiceConnectionStatusEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def voice_connection_status_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_voice_connection_status`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the voice connection status event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.voice.VoiceConnectionStatusEvent`]]
        ``on_voice_connection_status`` and a ``VoiceConnectionStatusEvent``
    """
    return "on_voice_connection_status", [
        VoiceConnectionStatusEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return voice_connection_status_middleware
