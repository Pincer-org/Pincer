# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when the user clicks a Rich Presence spectate invite in chat to
spectate a game
"""


from ..core.dispatch import GatewayDispatch
from ..utils.types import Coro


async def activity_spectate_middleware(self, payload: GatewayDispatch):
    """|coro|
    
    Middleware for ``on_activity_spectate`` event.
    
    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.
        
    payload : :class:`GatewayDispatch`
        The data received from the activity spectate event.
        
    Returns
    -------
    Tuple[:class:`str`, List[:class:`str`]]
        ``on_activity_spectate`` and a ``secret``
    """
    secret: str = payload.data.get("secret")
    return "on_activity_spectate", [secret]


def export() -> Coro:
    return activity_spectate_middleware
