# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client joins a voice channel"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.voice import VoiceChannelSelectEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def voice_channel_select_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_voice_channel_select`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the voice channel select event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.voice.VoiceChannelSelectEvent`]]
        ``on_voice_channel_select`` and a ``VoiceChannelSelectEvent``
    """
    return "on_voice_channel_select", [
        VoiceChannelSelectEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return voice_channel_select_middleware
