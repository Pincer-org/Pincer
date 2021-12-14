# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user started typing in a channel"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.typing_start import TypingStartEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def typing_start_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_typing_start`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the typing start event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.typing_start.TypingStartEvent`]
        ``on_typing_start`` and a ``TypingStartEvent``
    """  # noqa: E501
    return (
        "on_typing_start",
        TypingStartEvent.from_dict(construct_client_dict(self, payload.data)),
    )


def export() -> Coro:
    return typing_start_middleware
