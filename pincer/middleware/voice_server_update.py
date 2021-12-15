# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild's voice server is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.voice import VoiceServerUpdateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def voice_server_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_voice_server_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the voice server update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.voice.VoiceServerUpdateEvent`]
        ``on_voice_server_update`` and a ``VoiceServerUpdateEvent``
    """  # noqa: E501
    return (
        "on_voice_server_update",
        VoiceServerUpdateEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return voice_server_update_middleware
