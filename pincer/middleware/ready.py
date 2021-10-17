# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent immediately after connecting,
contains server information
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import Tuple
    from ..utils.types import Coro
    from ..objects.user.user import User
    from ..commands import ChatCommandHandler
    from ..core.dispatch import GatewayDispatch


async def on_ready_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str]:
    """|coro|

    Middleware for ``on_ready`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    :class:`str`
        ``on_ready``
    """
    user = payload.data.get("user")

    if not user:
        raise InvalidPayload(
            "A `user` key/value pair is expected on the `ready` payload "
            "event."
        )  # TODO this error doesn't exist???

    self.bot = User.from_dict(construct_client_dict(self, user))

    await ChatCommandHandler(self).initialize()
    return "on_ready",


def export() -> Coro:
    return on_ready_middleware
