# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Optional, Union

    from ..user.user import User
    from ..guild.member import GuildMember
    from ...utils.snowflake import Snowflake
    from ..app.command import ClientCommandStructure


@dataclass
class MessageContext:
    """
    Represents the context of a message interaction.

    :param id:
        The ID of the interaction.

    :param author:
        The user whom invoked the interaction.

    :param command:
        The local command object for the command to whom this context
        belongs.

    :param guild_id:
        The ID of the guild the interaction was invoked in.
        Can be None if it wasn't invoked in a guild.

    :param channel_id:
        The ID of the channel the interaction was invoked in.
        Can be None if it wasn't invoked in a channel.
    """
    id: Snowflake
    author: Union[GuildMember, User]
    command: ClientCommandStructure

    guild_id: Optional[Snowflake] = None
    channel_id: Optional[Snowflake] = None
