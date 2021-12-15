# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user joins a subscribed voice channel"""

from ..core.dispatch import GatewayDispatch
from ..objects.user import VoiceState
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def voice_state_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_voice_state_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the voice state create event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.user.voice_state.VoiceState`]
        ``on_voice_state_create`` and a ``VoiceState``
    """
    return (
        "on_voice_state_create",
        VoiceState.from_dict(construct_client_dict(self, payload.data)),
    )


def export() -> Coro:
    return voice_state_create_middleware
