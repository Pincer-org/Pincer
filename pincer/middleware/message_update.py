# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is updated in a subscribed text channel"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..core.dispatch import GatewayDispatch
    from ..objects import UserMessage


async def message_update_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[UserMessage]]:
    """|coro|

    Middleware for ``?`` event. # TODO ``?`` here because idk what it is

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.
    """
    return "on_message_update", [
        UserMessage.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]


def export():
    return message_update_middleware
