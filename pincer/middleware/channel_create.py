# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is created/joined on the client"""
from typing import List, Tuple

from ..core.dispatch import GatewayDispatch
from ..objects.guild.channel import Channel


def channel_create_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[Channel]]:
    """|coro|

    Middleware for ``on_channel_creation`` event.

    Parameters
    ----------
    payload : GatewayDispatch
        The data received from the ready event.
    """
    return "on_channel_creation",  [
        Channel.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]
