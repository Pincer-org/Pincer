# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the thread member object for the current user is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects import ThreadMember
from ..utils import Timestamp
from ..utils.conversion import construct_client_dict


async def thread_member_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_thread_member_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the thread member update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.thread.ThreadMember`]]
        ``on_thread_member_update`` and an ``ThreadMember``
    """

    return "on_thread_member_update", [
        ThreadMember.from_dict(construct_client_dict(
            self,
            {
                "join_timestamp": Timestamp(payload.data.pop("join_timestamp")),
                **payload.data
            }
        ))
    ]


def export():
    return thread_member_update_middleware
