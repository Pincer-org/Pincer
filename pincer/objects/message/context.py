# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from typing import Optional, Union
    from .user_message import UserMessage
    from ..app import ClientCommandStructure, Interaction
    from ..app.interaction_flags import InteractionFlags
    from ..guild.member import GuildMember
    from ..user.user import User
    from ...utils.convert_message import MessageConvertable
    from ...utils.snowflake import Snowflake


@dataclass
class MessageContext:
    """Represents the context of a message interaction.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The ID of the interaction.
    author: Union[:class:`~pincer.objects.guild.member.GuildMember`, :class:`~pincer.objects.user.user.User`]

        The user whom invoked the interaction.
    command: :class:`~pincer.objects.app.command.ClientCommandStructure`
        The local command object for the command to whom this context
        belongs.

    guild_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The ID of the guild the interaction was invoked in.
        Can be None if it wasn't invoked in a guild.
    channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The ID of the channel the interaction was invoked in.
        Can be None if it wasn't invoked in a channel.
    """
    # noqa: E501
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
        times after each other. (first one will always be the main
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
