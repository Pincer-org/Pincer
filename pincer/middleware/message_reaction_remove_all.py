# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user explicitly removes all reactions from a message."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.message import MessageReactionRemoveAllEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_remove_all_middleware(
    self,
    payload: GatewayDispatch
):
    """|coro|

    Middleware for ``on_message_reaction_remove_all`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the message reaction remove all event.


    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.message.MessageReactionRemoveAllEvent`]]
        ``on_message_reaction_remove_all`` and an ``MessageReactionRemoveAllEvent``
    """

    return "on_message_reaction_remove_all", [
        MessageReactionRemoveAllEvent.from_dict(
            construct_client_dict(self, payload.data)
        )
    ]


def export():
    return message_reaction_remove_all_middleware
