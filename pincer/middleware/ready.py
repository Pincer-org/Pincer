# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent immediately after connecting,
contains server information
"""

from ..commands import ChatCommandHandler
from ..core.dispatch import GatewayDispatch
from ..objects import User
from ..utils import Coro


async def on_ready_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_ready`` event.

    :param self:
        The current client.

    :param payload:
        The data received from the ready event.
    """
    self.bot = User.from_dict(
        {"_client": self, "_http": self.http,  **payload.data.get("user")}
    )
    await ChatCommandHandler(self).initialize()
    return "on_ready",


def export() -> Coro:
    return on_ready_middleware
