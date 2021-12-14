# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the thread member object for the current user is updated"""
from typing import Union

from ..core.dispatch import GatewayDispatch
from ..objects import ThreadMember
from ..utils import Timestamp
from ..utils.conversion import construct_client_dict


async def thread_member_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_thread_member_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the thread member update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.thread.ThreadMember`]
        ``on_thread_member_update`` and an ``ThreadMember``
    """
    join_timestamp: Union[str, float, int] = payload.data.get("join_timestamp")

    return (
        "on_thread_member_update",
        ThreadMember.from_dict(construct_client_dict(
            self,
            {
                "join_timestamp": Timestamp(join_timestamp),
                **payload.data
            }
        ))
    )


def export():
    return thread_member_update_middleware
