# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, TYPE_CHECKING
from asyncio import gather, iscoroutine

from ... import client
from ..user.user import User
from ..guild.role import Role
from . import interaction_base
from ...utils.types import MISSING
from ...core.http import HTTPClient
from ..guild.channel import Channel
from ..guild.member import GuildMember
from ...utils.types import APINullable
from ...utils.snowflake import Snowflake
from ...utils.api_object import APIObject
from ..app.select_menu import SelectOption
from ..message.user_message import UserMessage
from .command import AppCommandInteractionDataOption, AppCommandOptionType

if TYPE_CHECKING:
    from ...utils.conversion import convert
    from ..message.context import MessageContext


class InteractionFlags(IntEnum):
    """Represents the valid flags for interactions
    """
    EPHEMERAL = 1 << 6 #: Only the user receiving the message can see it


@dataclass
class ResolvedData(APIObject):
    """Represents a Discord Resolved Data structure

    Attributes
    ----------
    users: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.Dict`\\[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.user.user.User`]]
        Map of Snowflakes to user objects
    members: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.Dict`\\[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.member.GuildMember`]]
        Map of Snowflakes to partial member objects
    roles: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.Dict`\\[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.role.Role`]]
        Map of Snowflakes to role objects
    channels: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.Dict`\\[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.guild.channel.Channel`]]
        Map of Snowflakes to partial channel objects
    messages: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.Dict`\\[:class:`~pincer.utils.snowflake.Snowflake`, :class:`~pincer.objects.message.user_message.UserMessage`]]
        Map of Snowflakes to partial message objects
    """
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
    resolved: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.app.interactions.ResolvedData`]
        Converted users + roles + channels
    options: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.app.command.AppCommandInteractionDataOption`]
        The params + values from the user
    custom_id: :class:`~pincer.utils.types.APINullable`\\[:class:`str`]
        The `custom_id` of the component
    component_type: :class:`~pincer.utils.types.APINullable`\\[:class:`int`]
        The type of the component
    values: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.app.select_menu.SelectOption`]
        The values the user selected
    target_id: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the user or message targeted by a user or message command
    """
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
    data: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.app.interactions.InteractionData`]
        The command data payload
    guild_id: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        The guild it was sent from
    channel_id: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        The channel it was sent from
    member: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.guild.member.GuildMember`]
        Guild member data for the invoking user, including permissions
    user: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.user.user.User`]
        User object for the invoking user, if invoked in a DM
    message: :class:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.message.user_message.UserMessage`]
        For components, the message they were attached to
    """

    _client: client.Client
    _http: HTTPClient

    id: Snowflake
    application_id: Snowflake
    type: interaction_base.InteractionType
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
        self.type = convert(self.type, interaction_base.InteractionType)
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
