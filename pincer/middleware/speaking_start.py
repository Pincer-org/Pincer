# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user in a subscribed voice channel speaks"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.voice import SpeakingStartEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def speaking_start_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_speaking_start`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the speaking start event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`SpeakingStartEvent`]]
        ``on_speaking_start`` and a ``SpeakingStartEvent``
    """
    return "on_speaking_start", [
        SpeakingStartEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return speaking_start_middleware
