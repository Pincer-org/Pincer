# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""

from ..core.dispatch import GatewayDispatch
from ..objects.user import VoiceState


async def voice_state_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_voice_state_update`` event.

    :param self:
        The current client.

    :param payload:
        The data received from the ready event.

    """
    return "on_voice_state_update", [
        VoiceState.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]


def export():
    return voice_state_update_middleware
