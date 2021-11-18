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
from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import Tuple
    from ..utils.types import Coro
    from ..core.dispatch import GatewayDispatch


async def on_ready_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str]:
    """|coro|

    Middleware for ``on_ready`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the stage instance create event

    Returns
    -------
    Tuple[:class:`str`]
        ``on_ready``
    """
    user = payload.data.get("user")
    guilds = payload.data.get("guilds")

    if not user or guilds is None:
        raise InvalidPayload(
            "A `user` and `guilds` key/value pair is expected on the "
            "`ready` payload event."
        )

    self.bot = User.from_dict(construct_client_dict(self, user))
    self.guilds = dict(map(lambda i: (i["id"], None), guilds))

    await ChatCommandHandler(self).initialize(
        self.remove_unused_commands,
        self.update_existing_commands
    )
    return "on_ready",


def export() -> Coro:
    return on_ready_middleware
