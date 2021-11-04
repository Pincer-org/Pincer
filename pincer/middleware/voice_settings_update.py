# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client's voice settings update"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.voice_settings import VoiceSettingsUpdateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def voice_settings_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_voice_settings_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the voice settings update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.VoiceSettingsUpdateEvent`]]
        ``on_voice_settings_update`` and a ``VoiceSettingsUpdateEvent``
    """
    return "on_voice_settings_update", [
        VoiceSettingsUpdateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return voice_settings_update_middleware
