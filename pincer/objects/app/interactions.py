# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from asyncio import sleep, ensure_future
from dataclasses import dataclass
from typing import Any, Dict, TYPE_CHECKING, Union, Optional, List

from pincer.utils.api_object import ChannelProperty, GuildProperty
from .command_types import AppCommandOptionType
from .interaction_base import InteractionType, CallbackType
from .mentionable import Mentionable
from ..guild.member import GuildMember
from ..message.context import MessageContext
from ..message.message import Message
from ..message.user_message import UserMessage
from ..user import User
from ...exceptions import (
    InteractionDoesNotExist,
    UseFollowup,
    InteractionAlreadyAcknowledged,
    NotFoundError,
    InteractionTimedOut,
)
from ...utils import APIObject
from ...utils.convert_message import convert_message
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING

if TYPE_CHECKING:
    from .interaction_flags import InteractionFlags
    from ...utils.convert_message import MessageConvertable
    from .command import AppCommandInteractionDataOption
    from ..guild.channel import Channel
    from ..guild.role import Role
    from ...utils import APINullable


@dataclass(repr=False)
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
    """

    # noqa: E501
    users: APINullable[Dict[Snowflake, User]] = MISSING
    members: APINullable[Dict[Snowflake, GuildMember]] = MISSING
    roles: APINullable[Dict[Snowflake, Role]] = MISSING
    channels: APINullable[Dict[Snowflake, Channel]] = MISSING
    messages: APINullable[Dict[Snowflake, UserMessage]] = MISSING


@dataclass(repr=False)
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

    id: APINullable[Snowflake] = MISSING
    name: APINullable[str] = MISSING
    type: APINullable[int] = MISSING
    resolved: APINullable[ResolvedData] = MISSING
    options: APINullable[List[AppCommandInteractionDataOption]] = MISSING
    custom_id: APINullable[str] = MISSING
    component_type: APINullable[int] = MISSING
    values: APINullable[List[str]] = MISSING
    target_id: APINullable[Snowflake] = MISSING


@dataclass(repr=False)
class Interaction(APIObject, ChannelProperty, GuildProperty):
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
    """

    # noqa: E501
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
    has_replied: bool = False
    has_acknowledged: bool = False

    def __post_init__(self):
        super().__post_init__()

        if not self.data.options:
            return

        for option in self.data.options:
            if option.type is AppCommandOptionType.STRING:
                option.value = str(option.value)
            elif option.type is AppCommandOptionType.INTEGER:
                option.value = int(option.value)
            elif option.type is AppCommandOptionType.BOOLEAN:
                option.value = bool(option.value)
            elif option.type is AppCommandOptionType.NUMBER:
                option.value = float(option.value)

            elif option.type is AppCommandOptionType.USER:
                user = self.return_type(option, self.data.resolved.members)
                user.set_user_data(
                    self.return_type(option, self.data.resolved.users)
                )
                option.value = user

            elif option.type is AppCommandOptionType.CHANNEL:
                option.value = self.return_type(
                    option, self.data.resolved.channels
                )

            elif option.type is AppCommandOptionType.ROLE:
                option.value = self.return_type(
                    option, self.data.resolved.roles
                )

            elif option.type is AppCommandOptionType.MENTIONABLE:
                user = self.return_type(option, self.data.resolved.members)
                if user:
                    user.set_user_data(
                        self.return_type(option, self.data.resolved.users)
                    )

                option.value = Mentionable(
                    user, self.return_type(option, self.data.resolved.roles)
                )

    @staticmethod
    def return_type(
        option: Snowflake, data: Dict[Snowflake, Any]
    ) -> Optional[APIObject]:
        """
        Returns a value from the option or None if it doesn't exist.

        option : :class:`~pincer.utils.types.Snowflake`
            Snowflake to search ``data`` for.
        data : Dict[:class:`~pincer.utils.types.Snowflake`, Any]
            Resolved data to search through.
        """
        return data[option.value] if data else None

    def get_message_context(self):
        return MessageContext(
            self._client,
            self.member or self.user,
            self,
            self.guild_id,
            self.channel_id,
        )

    async def response(self) -> UserMessage:
        """|coro|

        Gets the original response for an interaction.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The fetched response!
        """
        if not self.has_replied:
            raise InteractionDoesNotExist(
                "No interaction reply has been sent yet!"
            )

        resp = await self._http.get(
            f"/webhooks/{self._client.bot.id}/{self.token}/messages/@original"
        )
        return UserMessage.from_dict(resp)

    async def _base_ack(
        self, flags: Optional[InteractionFlags], callback_type: CallbackType
    ):
        """|coro|

        Acknowledge an interaction, any flags here are applied to the reply.

        Parameters
        ----------
        message_type : :class:`~pincer.objects.app.interaction_base.CallbackType`
            The type of the message. Should be ``DEFERRED_MESSAGE`` or
            ``DEFERRED_UPDATE_MESSAGE``.
        flags: :class:`~pincer.objects.app.interaction_flags.InteractionFlags`
            The flags which must be applied to the reply.

        Raises
        ------
        :class:`~pincer.exceptions.InteractionAlreadyAcknowledged`
            The interaction was already acknowledged, this can be
            because a reply or ack was already sent.
        """
        if self.has_replied or self.has_acknowledged:
            raise InteractionAlreadyAcknowledged(
                "The interaction you are trying to acknowledge has already "
                "been acknowledged"
            )

        self.has_acknowledged = True
        await self._http.post(
            f"interactions/{self.id}/{self.token}/callback",
            {"type": callback_type, "data": {"flags": flags}},
        )

    async def ack(self, flags: Optional[InteractionFlags] = None):
        """|coro|

        Acknowledge an interaction, any flags here are applied to the reply.

        Parameters
        ----------
        flags :class:`~pincer.objects.app.interaction_flags.InteractionFlags`
            The flags which must be applied to the reply. |default| :data:`None`
        """
        return await self._base_ack(flags, CallbackType.DEFERRED_MESSAGE)

    async def deferred_update_ack(
        self, flags: Optional[InteractionFlags] = None
    ):
        """|coro|
        Same as ack but for updating a message.

        Parameters
        ----------
        flags :class:`~pincer.objects.app.interaction_flags.InteractionFlags`
            The flags which must be applied to the reply. |default| :data:`None`
        """
        return await self._base_ack(flags, CallbackType.DEFERRED_UPDATE_MESSAGE)

    async def __post_send_handler(self, message: Message):
        """Process the interaction after it was sent.

        Parameters
        ----------
        message :class:`~pincer.objects.message.message.Message`
            The interaction message.
        """

        if message.delete_after:
            await sleep(message.delete_after)
            await self.delete()

    def __post_sent(self, message: Message):
        """Ensure the `__post_send_handler` method its future.

        Parameters
        ----------
        message :class:`~pincer.objects.message.message.Message`
            The interaction message.
        """
        self.has_replied = True
        ensure_future(self.__post_send_handler(message))

    async def _base_reply(
        self,
        message: MessageConvertable,
        message_type: CallbackType,
        allow_empty: bool,
    ):
        """|coro|

        Initial reply, only works if no ACK has been sent yet.

        Parameters
        ----------
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The response message!
        message_type : :class:`~pincer.objects.app.interaction_base.CallbackType`
            The type of the message. Should be ``MESSAGE`` or
            ``UPDATE_MESSAGE``.

        Raises
        ------
        :class:`~.pincer.errors.UseFollowup`
            Exception raised when a reply has already been sent so a
            :func:`~pincer.objects.app.interactions.Interaction.followup`
            should be used instead.
        :class:`~.pincer.errors.InteractionTimedOut`
            Exception raised when discord had to wait too long for a reply.
            You can extend the discord wait time by using the
            :func:`~pincer.objects.app.interaction.Interaction.ack`
            function.
        """
        if self.has_replied:
            raise UseFollowup(
                "A response has already been sent to the interaction. "
                "Please use a followup instead!"
            )
        elif self.has_acknowledged:
            self.has_replied = True
            await self.edit(message)
            return

        message = convert_message(self._client, message)
        content_type, data = message.serialize(
            message_type=message_type, allow_empty=allow_empty
        )

        try:
            await self._http.post(
                f"interactions/{self.id}/{self.token}/callback",
                data,
                content_type=content_type,
            )
        except NotFoundError:
            raise InteractionTimedOut(
                "Discord had to wait too long for the interaction reply, "
                "you can extend the time it takes for discord to timeout by "
                "acknowledging the interaction. (using interaction.ack)"
            )

        self.__post_sent(message)

    async def reply(self, message: MessageConvertable) -> UserMessage:
        """|coro|
        Sends a reply to an interaction.
        """
        return await self._base_reply(message, CallbackType.MESSAGE, False)

    async def update(self, message: MessageConvertable) -> UserMessage:
        """|coro|
        Edits the reply to an interaction. Only works with Message Component
        Interactions.
        """
        return await self._base_reply(
            message, CallbackType.UPDATE_MESSAGE, True
        )

    async def edit(self, message: MessageConvertable) -> UserMessage:
        """|coro|

        Edit an interaction. This is also the way to reply to
        interactions whom have been acknowledged.

        Parameters
        ----------
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The new message!

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The updated message object.

        Raises
        ------
        :class:`~.pincer.errors.InteractionDoesNotExist`
            Exception raised when no reply has been sent.
        """

        if not self.has_replied:
            raise InteractionDoesNotExist(
                "The interaction whom you are trying to edit has not "
                "been sent yet!"
            )

        message = convert_message(self._client, message)
        content_type, data = message.serialize()

        resp = await self._http.patch(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/@original",
            data,
            content_type=content_type,
        )
        self.__post_sent(message)
        return UserMessage.from_dict(resp)

    async def delete(self):
        """|coro|

        Delete the interaction.

        Raises
        ------
        :class:`~pincer.errors.InteractionDoesNotExist`
            Exception raised when no reply has been sent.
        """
        if not self.has_replied:
            raise InteractionDoesNotExist(
                "The interaction whom you are trying to delete has not "
                "been sent yet!"
            )

        await self._http.delete(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/@original"
        )

    async def __post_followup_send_handler(
        self, followup: UserMessage, message: Message
    ):
        """Process a followup after it was sent.

        Parameters
        ----------
        followup :class:`~pincer.objects.message.user_message.UserMessage`
            The followup message that is being post processed.
        message :class:`~pincer.objects.message.message.Message`
            The followup message.
        """

        if message.delete_after:
            await sleep(message.delete_after)
            await self.delete_followup(followup.id)

    def __post_followup_sent(self, followup: UserMessage, message: Message):
        """Ensure the `__post_followup_send_handler` method its future.

        Parameters
        ----------
        followup :class:`~pincer.objects.message.user_message.UserMessage`
            The followup message that is being post processed.
        message :class:`~pincer.objects.message.message.Message`
            The followup message.
        """
        ensure_future(self.__post_followup_send_handler(followup, message))

    async def followup(self, message: MessageConvertable) -> UserMessage:
        """|coro|

        Create a follow-up message for the interaction.
        This allows you to respond with multiple messages.

        Parameters
        ----------
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The message to send.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The message that has been sent.
        """
        message = convert_message(self._client, message)
        content_type, data = message.serialize()

        resp = await self._http.post(
            f"webhooks/{self._client.bot.id}/{self.token}",
            data,
            content_type=content_type,
        )
        msg = UserMessage.from_dict(resp)
        self.__post_followup_sent(msg, message)
        return msg

    async def edit_followup(
        self, message_id: int, message: MessageConvertable
    ) -> UserMessage:
        """|coro|

        Edit a followup message.

        Parameters
        ----------
        message_id :class:`int`
            The id of the original followup message.
        message :class:`~pincer.utils.convert_message.MessageConvertable`
            The message new message.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The updated message object.
        """
        message = convert_message(self._client, message)
        content_type, data = message.serialize()

        resp = await self._http.patch(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
            data,
            content_type=content_type,
        )
        msg = UserMessage.from_dict(resp)
        self.__post_followup_sent(msg, message)
        return msg

    async def get_followup(self, message_id: int) -> UserMessage:
        """|coro|

        Get a followup message by id.

        Parameters
        ----------
        message_id :class:`int`
            The id of the original followup message that must be fetched.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The fetched message object.
        """

        resp = await self._http.get(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
        )
        return UserMessage.from_dict(resp)

    async def delete_followup(self, message: Union[UserMessage, int]):
        """|coro|

        Remove a followup message by id.

        Parameters
        ----------
        message Union[:class:`~pincer.objects.user_message.UserMessage`, :class:`int`]
            The id/followup object of the followup message that must be deleted.
        """
        message_id = message if isinstance(message, int) else message.id

        await self._http.delete(
            f"webhooks/{self._client.bot.id}/{self.token}/messages/{message_id}",
        )
