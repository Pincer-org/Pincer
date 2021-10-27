# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING
from asyncio import gather, iscoroutine

from ..user.user import User
from ...utils.types import MISSING
from ..guild.member import GuildMember
from ...utils.conversion import convert
from ...utils.snowflake import Snowflake
from ...utils.api_object import APIObject
from ..app.select_menu import SelectOption
from ..message.context import MessageContext
from .interaction_base import InteractionType
from ..message.user_message import UserMessage
from .command import AppCommandInteractionDataOption, AppCommandOptionType

if TYPE_CHECKING:
    from ..guild.role import Role
    from ..guild.channel import Channel
    from ...utils.types import APINullable


class InteractionFlags(IntEnum):
    """Represents the valid flags for interactions

    Attributes
    ----------
    EPHEMERAL:
        Only the user receiving the message can see it.
    """
    EPHEMERAL = 1 << 6


@dataclass
class ResolvedData(APIObject):
    """Represents a Discord Resolved Data structure

    Attributes
    ----------
    users: APINullable[Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.user.user.User`]]
        Map of Snowflakes to user objects
    members: APINullable[Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.member.GuildMember`]]
        Map of Snowflakes to partial member objects
    roles: APINullable[Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.role.Role`]]
        Map of Snowflakes to role objects
    channels: APINullable[Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.channel.Channel`]]
        Map of Snowflakes to partial channel objects
    messages: APINullable[Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.message.user_message.UserMessage`]]
        Map of Snowflakes to partial message objects
    """  # noqa: E501
    users: APINullable[Dict[Snowflake, User]] = MISSING
    members: APINullable[Dict[Snowflake, GuildMember]] = MISSING
    roles: APINullable[Dict[Snowflake, Role]] = MISSING
    channels: APINullable[Dict[Snowflake, Channel]] = MISSING
    messages: APINullable[Dict[Snowflake, UserMessage]] = MISSING


@dataclass
class InteractionData(APIObject):
    """Represents a Discord Interaction Data structure

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The `ID` of the invoked command
    name: :class:`str`
        The `name` of the invoked command
    type: :class:`int`
        The `type` of the invoked command
    resolved: APINullable[:class:`~pincer.objects.app.interactions.ResolvedData`]
        Converted users + roles + channels
    options: APINullable[:class:`~pincer.objects.app.command.AppCommandInteractionDataOption`]
        The params + values from the user
    custom_id: APINullable[:class:`str`]
        The `custom_id` of the component
    component_type: APINullable[:class:`int`]
        The type of the component
    values: APINullable[:class:`~pincer.objects.app.select_menu.SelectOption`]
        The values the user selected
    target_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the user or message targeted by a user or message command
    """  # noqa: E501
    id: Snowflake
    name: str
    type: int

    resolved: APINullable[ResolvedData] = MISSING
    options: APINullable[AppCommandInteractionDataOption] = MISSING
    custom_id: APINullable[str] = MISSING
    component_type: APINullable[int] = MISSING
    values: APINullable[SelectOption] = MISSING
    target_id: APINullable[Snowflake] = MISSING

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
        self.resolved = convert(
            self.resolved,
            ResolvedData.from_dict,
            ResolvedData
        )
        self.options = convert(
            self.options,
            AppCommandInteractionDataOption.from_dict,
            AppCommandInteractionDataOption
        )
        self.values = convert(
            self.values,
            SelectOption.from_dict,
            SelectOption
        )
        self.target_id = convert(self.target_id, Snowflake.from_string)


@dataclass
class Interaction(APIObject):
    """Represents a Discord Interaction object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the interaction
    application_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the application this interaction is for
    type: :class:`~pincer.objects.app.interaction_base.InteractionType`
        The type of interaction
    token: :class:`str`
        A continuation token for responding to the interaction
    version: :class:`int`
        Read-only property, always ``1``
    data: APINullable[:class:`~pincer.objects.app.interactions.InteractionData`]
        The command data payload
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The guild it was sent from
    channel_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The channel it was sent from
    member: APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
        Guild member data for the invoking user, including permissions
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        User object for the invoking user, if invoked in a DM
    message: APINullable[:class:`~pincer.objects.message.user_message.UserMessage`]
        For components, the message they were attached to
    """  # noqa: E501
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    token: str

    version: int = 1
    data: APINullable[InteractionData] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    channel_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
    user: APINullable[User] = MISSING
    message: APINullable[UserMessage] = MISSING

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
        self.application_id = convert(
            self.application_id, Snowflake.from_string
        )
        self.type = convert(self.type, InteractionType)
        self.data = convert(
            self.data,
            InteractionData.from_dict,
            InteractionData
        )
        self.guild_id = convert(self.guild_id, Snowflake.from_string)
        self.channel_id = convert(self.channel_id, Snowflake.from_string)

        self.member = convert(
            self.member,
            GuildMember.from_dict,
            GuildMember,
            client=self._client
        )

        self.user = convert(
            self.user,
            User.from_dict,
            User,
            client=self._client
        )

        self.message = convert(
            self.message,
            UserMessage.from_dict,
            UserMessage,
            client=self._client
        )

        self._convert_functions = {
            AppCommandOptionType.SUB_COMMAND: None,
            AppCommandOptionType.SUB_COMMAND_GROUP: None,

            AppCommandOptionType.STRING: str,
            AppCommandOptionType.INTEGER: int,
            AppCommandOptionType.BOOLEAN: bool,
            AppCommandOptionType.NUMBER: float,

            AppCommandOptionType.USER: lambda value:
                self._client.get_user(
                    convert(value, Snowflake.from_string)
                ),
            AppCommandOptionType.CHANNEL: lambda value:
                self._client.get_channel(
                    convert(value, Snowflake.from_string)
                ),
            AppCommandOptionType.ROLE: lambda value:
                self._client.get_role(
                    convert(self.guild_id, Snowflake.from_string),
                    convert(value, Snowflake.from_string)
                ),
            AppCommandOptionType.MENTIONABLE: None
        }

    async def build(self):
        """|coro|

        Sets the parameters in the interaction that need information from the
        discord API.
        """
        if not self.data.options:
            return

        await gather(
            *map(self.convert, self.data.options)
        )

    async def convert(self, option: AppCommandInteractionDataOption):
        """|coro|

        Sets an AppCommandInteractionDataOption value paramater to the payload
        type
        """
        converter = self._convert_functions.get(option.type)

        if not converter:
            raise NotImplementedError(
                f"Handling for AppCommandOptionType {option.type} is not "
                "implemented"
            )

        res = converter(option.value)

        if iscoroutine(res):
            option.value = await res
            return

        option.value = res

    def convert_to_message_context(self, command):
        return MessageContext(
            self.id,
            self.member or self.user,
            command,
            self.guild_id,
            self.channel_id
        )
