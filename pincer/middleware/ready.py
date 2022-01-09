# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent immediately after connecting,
contains server information
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..commands import ChatCommandHandler
from ..exceptions import InvalidPayload
from ..objects.user.user import User

if TYPE_CHECKING:
    from typing import Tuple
    from ..utils.types import Coro
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def on_ready_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str]:
    """|coro|

    Middleware for the ``on_ready`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the stage instance create event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`]
        ``on_ready``
    """

    gateway.set_session_id(payload.data.get("session_id"))

    user = payload.data.get("user")
    guilds = payload.data.get("guilds")

    if not user or guilds is None:
        raise InvalidPayload(
            "A `user` and `guilds` key/value pair is expected on the "
            "`ready` payload event."
        )

    self.bot = User.from_dict(user)
    self.guilds = dict(map(lambda i: (i["id"], None), guilds))

    await ChatCommandHandler(self).initialize()
    return ("on_ready",)


def export() -> Coro:
    return on_ready_middleware
