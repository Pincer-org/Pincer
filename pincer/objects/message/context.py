# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Optional, Union

    from ..app.command import ClientCommandStructure
    from ..guild.member import GuildMember
    from ..user.user import User
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
    """  # noqa: E501
    id: Snowflake
    author: Union[GuildMember, User]
    command: ClientCommandStructure

    guild_id: Optional[Snowflake] = None
    channel_id: Optional[Snowflake] = None
