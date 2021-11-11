# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user removes a reaction to a message"""

from ..core.dispatch import GatewayDispatch
from ..objects import Emoji
from ..objects.events.message import MessageReactionRemoveEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_remove_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_message_reaction_remove`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the message reaction remove event.


    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.message.MessageReactionRemoveEvent`]]
        ``on_message_reaction_remove`` and an ``MessageReactionRemoveEvent``
    """

    return "on_message_reaction_remove", [
        MessageReactionRemoveEvent.from_dict(
            construct_client_dict(
                self,
                {
                    "emoji": Emoji.from_dict(
                        construct_client_dict(self, payload.data.pop("emoji"))
                    ),
                    **payload.data
                }
            ))
    ]


def export():
    return message_reaction_remove_middleware
