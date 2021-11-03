# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when the user clicks a Rich Presence join invite in chat
to join a game.
"""

from ..core.dispatch import GatewayDispatch
from ..utils.types import Coro


async def activity_join_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_activity_join`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`GatewayDispatch`
        The data received from the activity join event.


    Returns
    -------
    Tuple[:class:`str`, List[:class:`str`]]
        ``on_activity_join`` and a ``secret``
    """
    secret: str = payload.data.get("secret")
    return "on_activity_join", [secret]


def export() -> Coro:
    return activity_join_middleware
