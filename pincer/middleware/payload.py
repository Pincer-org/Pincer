# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from ..core.dispatch import GatewayDispatch


async def payload_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_payload`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`GatewayDispatch`
        The data received from the notification create event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.core.dispatch.GatewayDispatch`]]
        ``on_payload`` and a ``GatewayDispatch`` object
    """
    return "on_payload", [payload]


def export():
    return payload_middleware
