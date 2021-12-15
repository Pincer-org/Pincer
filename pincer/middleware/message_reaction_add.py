# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user adds a reaction to a message"""

from ..core.dispatch import GatewayDispatch
from ..objects import GuildMember, Emoji
from ..objects.events.message import MessageReactionAddEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_add_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_message_reaction_add`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the message reaction add event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageReactionAddEvent`]
        ``on_message_reaction_add`` and an ``MessageReactionAddEvent``
    """  # noqa: E501

    return (
        "on_message_reaction_add",
        MessageReactionAddEvent.from_dict(
            construct_client_dict(
                self,
                {
                    "member": GuildMember.from_dict(
                        construct_client_dict(self, payload.data.pop("member"))
                    ),
                    "emoji": Emoji.from_dict(
                        construct_client_dict(self, payload.data.pop("emoji"))
                    ),
                    **payload.data,
                },
            )
        ),
    )


def export():
    return message_reaction_add_middleware
