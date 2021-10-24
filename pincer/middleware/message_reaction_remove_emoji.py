# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a bot removes all instances of a given emoji from the reactions of a message"""

from ..core.dispatch import GatewayDispatch
from ..objects import Emoji
from ..objects.events.message import MessageReactionRemoveEmojiEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_remove_emoji_middleware(self,
                                                   payload: GatewayDispatch):
    """
    Middleware for ``on_message_reaction_remove_emoji``,
        creates a object for the message reaction emoji that is removed

    :param self:
        The current client.

    :param payload:
        The data received from the message reaction remove event.
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
