# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a bot removes all instances of a given emoji from the reactions of a message"""

from ..core.dispatch import GatewayDispatch
from ..objects import Emoji
from ..objects.events.message import MessageReactionRemoveEmojiEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_remove_emoji_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_message_reaction_remove_emoji`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the message reaction remove emoji event.


    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.message.MessageReactionRemoveEmojiEvent`]]
        ``on_message_reaction_remove_emoji`` and an ``MessageReactionRemoveEmojiEvent``
    """

    return "on_message_reaction_remove_emoji", [
        MessageReactionRemoveEmojiEvent.from_dict(
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
    return message_reaction_remove_emoji_middleware
