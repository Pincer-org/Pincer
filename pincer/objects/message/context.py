# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from ..app.interaction_flags import InteractionFlags
    from ...utils.convert_message import MessageConvertable
    from .user_message import UserMessage
    from ..app import ClientCommandStructure, Interaction
    from ..guild.member import GuildMember
    from ..user import User
    from ...utils.snowflake import Snowflake


@dataclass
class MessageContext:
    """
    Represents the context of a message interaction.

    :param author:
        The user whom invoked the interaction.

    :param command:
        The local command object for the command to whom this context
        belongs.

    interaction :class:`~pincer.objects.app.interaction.Interaction`
        The interaction this command belongs to.

    :param guild_id:
        The ID of the guild the interaction was invoked in.
        Can be None if it wasn't invoked in a guild.

    :param channel_id:
        The ID of the channel the interaction was invoked in.
        Can be None if it wasn't invoked in a channel.
    """
    author: Union[GuildMember, User]
    command: ClientCommandStructure
    interaction: Interaction

    guild_id: Optional[Snowflake] = None
    channel_id: Optional[Snowflake] = None

    async def ack(self, flags: InteractionFlags):
        """|coro|

        Alias for :func:`~pincer.objects.app.interactions.Interaction.ack`.

        Parameters
        ----------
        flags :class:`~pincer.objects.app.interaction_flags.InteractionFlags`
            The flags which must be applied to the reply.
        """
        await self.interaction.ack(flags)

    async def reply(self, message: MessageConvertable):
        """|coro|

        Alias for :func:`~pincer.objects.app.interactions.Interaction.reply`.

        Parameters
        ----------
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The response message!
        """
        await self.interaction.reply(message)

    async def followup(self, message: MessageConvertable) -> UserMessage:
        """|coro|

        Alias for :func:`~pincer.objects.app.interactions.Interaction.followup`.

        Parameters
        ----------
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The message to sent.
        """
        return await self.interaction.followup(message)

    async def send(self, message: MessageConvertable) -> UserMessage:
        """|coro|

        Send a response for an interaction.
        This object returns the sent object and may be used several
        times after eachoter. (first one will always be the main
        interaction response)

        Uses
        ----
        :func:`~pincer.objects.message.context.MessageContext.reply`
            Method gets called for initial send.
        :func:`~pincer.objects.app.interactions.Interaction.response`
            Method gets called for initial send to get response.
        :func:`~pincer.objects.message.context.MessageContext.followup`
            Method gets called for second message and onwards.

         Returns
         -------
         :class:`~pincer.objects.message.user_message.UserMessage`
            The message that was sent.
        """
        if self.interaction.has_replied:
            return await self.followup(message)

        await self.reply(message)
        return await self.interaction.response()
