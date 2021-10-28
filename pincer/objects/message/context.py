# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union, TYPE_CHECKING


if TYPE_CHECKING:
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

    async def send(self, message: MessageConvertable):
        if self.interaction.has_replied:
            await self.interaction.followup(message)
        else:
            await self.interaction.reply(message)
