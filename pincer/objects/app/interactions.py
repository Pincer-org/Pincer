# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from asyncio import gather, iscoroutine, sleep, ensure_future
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

from .command_types import AppCommandOptionType
from .interaction_base import InteractionType, CallbackType
from ..app.select_menu import SelectOption
from ..guild.member import GuildMember
from ..message.context import MessageContext
from ..message.user_message import UserMessage
from ..user import User
from ...utils import APIObject, convert
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING

if TYPE_CHECKING:
    from .command import AppCommandInteractionDataOption
    from ..message.message import Message
    from ..guild.channel import Channel
    from ..guild.role import Role
    from ...utils import APINullable


@dataclass
class ResolvedData(APIObject):
    """
    Represents a Discord Resolved Data structure

    :param users:
        Map of Snowflakes to user objects

    :param members:
        Map of Snowflakes to partial member objects

    :param roles:
        Map of Snowflakes to role objects

    :param channels:
        Map of Snowflakes to partial channel objects

    :param messages:
        Map of Snowflakes to partial message objects
    """
    users: APINullable[Dict[Snowflake, User]] = MISSING
    members: APINullable[Dict[Snowflake, GuildMember]] = MISSING
    roles: APINullable[Dict[Snowflake, Role]] = MISSING
    channels: APINullable[Dict[Snowflake, Channel]] = MISSING
    messages: APINullable[Dict[Snowflake, UserMessage]] = MISSING


@dataclass
class InteractionData(APIObject):
    """
    Represents a Discord Interaction Data structure

    :param id:
        the `ID` of the invoked command

    :param name:
        the `name` of the invoked command

    :param type:
        the `type` of the invoked command

    :param resolved:
        converted users + roles + channels

    :param options:
        the params + values from the user

    :param custom_id:
        the `custom_id` of the component

    :param component_type:
        the type of the component

    :param values:
        the values the user selected

    :param target_id:
        id of the user or message targeted by a user or message command
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


@dataclass
class Interaction(APIObject):
    """
    Represents a Discord Interaction object

    :param id:
        id of the interaction

    :param application_id:
        id of the application this interaction is for

    :param type:
        the type of interaction

    :param data:
        the command data payload

    :param guild_id:
        the guild it was sent from

    :param channel_id:
        the channel it was sent from

    :param member:
        guild member data for the invoking user, including permissions

    :param user:
        user object for the invoking user, if invoked in a DM

    :param token:
        a continuation token for responding to the interaction

    :param version:
        read-only property, always `1`

    :param message:
        for components, the message they were attached to
    """
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
        """
        Sets the parameters in the interaction that need information from the
        discord API.
        """

        if not self.data.options:
            return

        await gather(
            *map(self.convert, self.data.options)
        )

    async def convert(self, option: AppCommandInteractionDataOption):
        """
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

    async def __post_send_handler(self, message: Message):
        """
        Process the interaction after it was sent.

        :param message:
            The interaction message.
        """

        if message.delete_after:
            await sleep(message.delete_after)
            await self.delete()

    def __post_sent(self, message: Message):
        """
        Ensure the `__post_send_handler` method its future.

        :param message:
            The interaction message.
        """
        ensure_future(self.__post_send_handler(message))

    async def reply(self, message: Message):
        """
        Initial reply, only works if no ACK has been sent yet.

        :param message:
            The response message!
        """
        content_type, data = message.serialize()

        await self._http.post(
            f"interactions/{self.id}/{self.token}/callback",
            {
                "type": CallbackType.MESSAGE,
                "data": data
            },
            content_type=content_type
        )
        self.__post_sent(message)

    async def edit(self, message: Message) -> UserMessage:
        """
        Edit an interaction. This is also the way to reply to
        interactions whom have been acknowledged.

        :param message:
            The new message!
        """
        content_type, data = message.serialize()

        resp = await self._http.patch(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/@original",
            data,
            content_type=content_type
        )
        self.__post_sent(message)
        return UserMessage.from_dict(resp)

    async def delete(self):
        """
        Delete the interaction.
        """
        await self._http.delete(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/@original"
        )

    async def __post_followup_send_handler(
            self,
            followup: UserMessage,
            message: Message
    ):
        """
        Process a folloup after it was sent.

        :param followup:
            The followup message that is being post processed.

        :param message:
            The interaction message.
        """

        if message.delete_after:
            await sleep(message.delete_after)
            await self.delete_followup(followup.id)

    def __post_followup_sent(
            self,
            followup: UserMessage,
            message: Message
    ):
        """
        Ensure the `__post_followup_send_handler` method its future.

        :param followup:
            The followup message that is being post processed.

        :param message:
            The followup message.
        """
        ensure_future(self.__post_followup_send_handler(followup, message))

    async def followup(self, message: Message) -> UserMessage:
        """
        Create a follow up message for the interaction.
        This allows you to respond with multiple messages.

        :param message:
            The message!
        """
        content_type, data = message.serialize()

        resp = await self._http.post(
            f"webhooks/{self._client.bot.id}/{self.token}",
            data,
            content_type=content_type
        )
        msg = UserMessage.from_dict(resp)
        self.__post_followup_sent(msg, message)
        return msg

    async def edit_followup(self, message_id: int, message: Message) \
            -> UserMessage:
        """
        Edit a followup message.

        :param message_id:
            The id of the original followup message.

        :param message:
            The new message!
        """
        content_type, data = message.serialize()

        resp = await self._http.patch(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
            data,
            content_type=content_type
        )
        msg = UserMessage.from_dict(resp)
        self.__post_followup_sent(msg, message)
        return msg

    async def get_followup(self, message_id: int) -> UserMessage:
        """
        Get a followup message by id.

        :param message_id:
            The id of the original followup message that must be fetched.
        """

        resp = await self._http.get(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
        )
        return UserMessage.from_dict(resp)

    async def delete_followup(self, message_id: int):
        """
        Remove a followup message by id.

        :param message_id:
            The id of the followup message that must be deleted.
        """

        await self._http.delete(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
        )
