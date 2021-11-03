# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user in a subscribed voice channel stops speaking"""

from ..core.dispatch import GatewayDispatch
from ..utils.snowflake import Snowflake
from ..utils.types import Coro


async def speaking_stop_middleware(self, payload: GatewayDispatch):
    """|coro|
    
    Middleware for ``on_speaking_stop`` event.
    
    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.
    payload : :class:`GatewayDispatch`
        The data received from the speaking stop event.
        
    Returns
    -------
    Tuple[:class:`str`, List[:class:`Snowflake`]]
        ``on_speaking_stop`` and a ``Snowflake`` (user_id)
    """
    user_id: Snowflake = Snowflake.from_string(payload.data.get("user_id"))
    return "on_speaking_stop", [user_id]


def export() -> Coro:
    return speaking_stop_middleware