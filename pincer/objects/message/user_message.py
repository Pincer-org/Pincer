# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import TYPE_CHECKING

from .attachment import Attachment
from .component import MessageComponent
from .embed import Embed
from .reaction import Reaction
from .reference import MessageReference
from .sticker import StickerItem
from ..app.application import Application
from ..app.interaction_base import MessageInteraction
from ..guild.member import GuildMember
from ..guild.role import Role
from ..user.user import User
from ..._config import GatewayConfig
from ...utils.api_object import APIObject
from ...utils.conversion import construct_client_dict
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Any, List, Optional, Union, Generator

    from ..guild.channel import Channel, ChannelMention
    from ...utils.types import APINullable
    from ...utils.timestamp import Timestamp


class AllowedMentionTypes(str, Enum):
    """The allowed mentions.

    Attributes
    ----------
    ROLES:
        Controls role mentions
    USERS:
        Controls user mentions
    EVERYONE:
        Controls @everyone and @here mentions
    """
    ROLES = "roles"
    USERS = "users"
    EVERYONE = "everyone"


@dataclass
class AllowedMentions(APIObject):
    """Represents the entities the client can mention

    Attributes
    ----------
    parse: List[:class:`~pincer.objects.message.user_message.AllowedMentionTypes`]
        An array of allowed mention types to parse from the content.
    roles: List[Union[:class:`~pincer.objects.guild.role.Role`, :class:`~pincer.utils.snowflake.Snowflake`]]
        List of ``Role`` objects or snowflakes of allowed mentions.
    users: List[Union[:class:`~pincer.objects.user.user.User` :class:`~pincer.utils.snowflake.Snowflake`]]
        List of ``user`` objects or snowflakes of allowed mentions.
    reply: :class:`bool`
        If replies should mention the author.
        |default| :data:`True`
    """  # noqa: E501

    parse: List[AllowedMentionTypes]
    roles: List[Union[Role, Snowflake]]
    users: List[Union[User, Snowflake]]
    reply: bool = True

    def to_dict(self):
        def get_str_id(obj: Union[Snowflake, User, Role]) -> str:
            if hasattr(obj, "id"):
                obj = obj.id

            return str(obj)

        return {
            "parse": self.parse,
            "roles": list(map(get_str_id, self.roles)),
            "users": list(map(get_str_id, self.users)),
            "replied_user": self.reply
        }


class MessageActivityType(IntEnum):
    """The activity people can perform on a rich presence activity.

    Such an activity could for example be a spotify listen.

    Attributes
    ----------
    JOIN:
        Invite to join.
    SPECTATE:
        Invite to spectate.
    LISTEN:
        Invite to listen along.
    JOIN_REQUEST:
        Request to join.
    """
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlags(IntEnum):
    """Special message properties.

    Attributes
    ----------
    CROSSPOSTED:
        The message has been published to subscribed
        channels (via Channel Following)
    IS_CROSSPOST:
        This message originated from a message
        in another channel (via Channel Following)
    SUPPRESS_EMBEDS:
        Do not include any embeds when serializing this message
    SOURCE_MESSAGE_DELETED:
        The source message for this crosspost
        has been deleted (via Channel Following)
    URGENT:
        This message came from the urgent message system
    HAS_THREAD:
        This message has an associated thread,
        with the same id as the message
    EPHEMERAL:
        This message is only visible to the user
        who invoked the Interaction
    LOADING:
        This message is an Interaction
        Response and the bot is "thinking"
    """
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7


class MessageType(IntEnum):
    """Represents the type of the message.

    Attributes
    ----------
    DEFAULT:
        Normal message.
    RECIPIENT_ADD:
        Recipient is added.
    RECIPIENT_REMOVE:
        Recipient is removed.
    CALL:
        A call is being made.
    CHANNEL_NAME_CHANGE:
        The group channel name is changed.
    CHANNEL_ICON_CHANGE:
        The group channel icon is changed.
    CHANNEL_PINNED_MESSAGE:
        A message is pinned.
    GUILD_MEMBER_JOIN:
        A member joined.
    USER_PREMIUM_GUILD_SUBSCRIPTION:
        A boost.
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1:
        A boost that reached tier 1.
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2:
        A boost that reached tier 2.
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3:
        A boost that reached tier 3.
    CHANNEL_FOLLOW_ADD:
        A channel is subscribed to.
    GUILD_DISCOVERY_DISQUALIFIED:
        The guild is disqualified from discovery,
    GUILD_DISCOVERY_REQUALIFIED:
        The guild is requalified for discovery.
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING:
        Warning about discovery violations.
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING:
        Final warning about discovery violations.
    THREAD_CREATED:
        A thread is created.
    REPLY:
        A message reply.
    APPLICATION_COMMAND:
        Slash command is used and responded to.
    THREAD_STARTER_MESSAGE:
        The initial message in a thread when its created off a message.
    GUILD_INVITE_REMINDER:
        ??
    """
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    APPLICATION_COMMAND = 20

    if GatewayConfig.version < 8:
        REPLY = 0
        APPLICATION_COMMAND = 0

    if GatewayConfig.version >= 9:
        THREAD_STARTER_MESSAGE = 21

    GUILD_INVITE_REMINDER = 22


@dataclass
class MessageActivity(APIObject):
    """Represents a Discord Message Activity object

    Attributes
    ----------
    type: :class:`~pincer.objects.message.user_message.MessageActivity`
        type of message activity
    party_id: APINullable[:class:`str`]
        party_id from a Rich Presence event
    """
    type: MessageActivityType
    party_id: APINullable[str] = MISSING


@dataclass
class UserMessage(APIObject):
    """Represents a message sent in a channel within Discord.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Ud of the message
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the channel the message was sent in
    author: :class:`~pincer.objects.user.user.User`
        The author of this message (not guaranteed to be a valid user)
    content: :class:`str`
        Contents of the message
    timestamp: :class:`~pincer.utils.timestamp.Timestamp`
        When this message was sent
    edited_timestamp: Optional[:class:`~pincer.utils.timestamp.Timestamp`]
        When this message was edited (or null if never)
    tts: :class:`bool`
        Whether this was a TTS message
    mention_everyone: :class:`bool`
        Whether this message mentions everyone
    mentions: List[:class:`~pincer.objects.guild.member.GuildMember`]
        Users specifically mentioned in the message
    mention_roles: List[:class:`~pincer.objects.guild.role.Role`]
        Roles specifically mentioned in this message
    attachments: List[:class:`~pincer.objects.message.attachment.Attachment`]
        Any attached files
    embeds: List[:class:`~pincer.objects.message.embed.Embed`]
        Any embedded content
    pinned: :class:`bool`
        Whether this message is pinned
    type: :class:`~pincer.objects.message.user_message.MessageType`
        Type of message
    mention_channels: APINullable[List[:class:`~pincer.objects.guild.channel.Channel`]]
        Channels specifically mentioned in this message
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the guild the message was sent in
    member: APINullable[:class:`~pincer.objects.guild.member.PartialGuildMember`]
        Member properties for this message's author
    reactions: APINullable[List[:class:`~pincer.objects.message.reaction.Reaction`]]
        Reactions to the message
    nonce: APINullable[Union[:class:`int`, :class:`str`]]
        User for validating a message was sent
    webhook_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        If the message is generated by a webhook,
        this is the webhook's id
    activity: APINullable[:class:`~pincer.objects.message.user_message.MessageActivity`]
        Sent with Rich Presence-related chat embeds
    application: APINullable[:class:`~pincer.objects.app.application.Application`]
        Sent with Rich Presence-related chat embeds
    application_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        If the message is a response to an Interaction,
        this is the id of the interaction's application
    message_reference: APINullable[:class:`~pincer.objects.message.reference.MessageReference`]
        Data showing the source of a crosspost,
        channel follow add, pin, or reply message
    flags: APINullable[:class:`~pincer.objects.message.user_message.MessageFlags`]
        Message flags combined as a bitfield
    referenced_message: APINullable[Optional[:class:`~pincer.objects.message.user_message.UserMessage`]]
        The message associated with the message_reference
    interaction: APINullable[:class:`~pincer.objects.app.interaction_base.MessageInteraction`]
        Sent if the message is a response to an Interaction
    thread: APINullable[:class:`~pincer.objects.guild.channel.Channel`]
        The thread that was started from this message,
        includes thread member object
    components: APINullable[List[:class:`~pincer.objects.message.component.MessageComponent`]]
        Sent if the message contains components like buttons,
        action rows, or other interactive components
    sticker_items: APINullable[List[:class:`~pincer.objects.message.sticker.StickerItem`]]
        Sent if the message contains stickers
    """
    # noqa: E501

    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: Timestamp
    tts: bool
    mention_everyone: bool
    mentions: List[GuildMember]
    mention_roles: List[Role]
    attachments: List[Attachment]
    embeds: List[Embed]
    pinned: bool
    type: MessageType

    edited_timestamp: APINullable[Timestamp] = MISSING
    mention_channels: APINullable[List[ChannelMention]] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
    reactions: APINullable[List[Reaction]] = MISSING
    nonce: APINullable[Union[int, str]] = MISSING
    webhook_id: APINullable[Snowflake] = MISSING
    activity: APINullable[MessageActivity] = MISSING
    application: APINullable[Application] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    message_reference: APINullable[MessageReference] = MISSING
    flags: APINullable[MessageFlags] = MISSING
    referenced_message: APINullable[Optional[UserMessage]] = MISSING
    interaction: APINullable[MessageInteraction] = MISSING
    thread: APINullable[Channel] = MISSING
    components: APINullable[List[MessageComponent]] = MISSING
    sticker_items: APINullable[List[StickerItem]] = MISSING

    def __str__(self):
        return self.content

    async def get_most_recent(self):
        """|coro|

        Certain Discord methods don't return the message object data after its
        updated. This function can be run to get the most recent version of the
        message object.
        """

        return self.from_dict(
            construct_client_dict(
                self._client,
                await self._http.get(
                    f"/channels/{self.channel_id}/messages/{self.id}"
                )
            )
        )

    async def react(self, emoji: str):
        """|coro|

        Create a reaction for the message. Requires the
        ``READ_MESSAGE_HISTORY` intent. ``ADD_REACTIONS`` intent is required if
        nobody else has reacted using the emoji.

        Parameters
        ----------
        emoji: :class:`str`
            Character for emoji. Does not need to be URL encoded.
        """

        await self._http.put(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
        )

    async def unreact(self, emoji: str):
        """|coro|

        Delete a reaction the current user has made for the message.

        Parameters
        ----------
        emoji: :class:`str`
            Character for emoji. Does not need to be URL encoded.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
        )

    async def remove_user_reaction(self, emoji: str, user_id: Snowflake):
        """|coro|

        Deletes another user's reaction. Requires the ``MANAGE_MESSAGES``
        intent.

        Parameters
        ----------
        emoji: :class:`str`
            Character for emoji. Does not need to be URL encoded.
        user_id: :class:`~pincer.utils.snowflake.Snowflake`
            User ID
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
            f"/{user_id}"
        )

    async def get_reactions(
        self, emoji: str, after: Snowflake = 0, limit=25
    ) -> Generator[User, None, None]:
        # TODO: HTTP Client will need to refactored to allow parameters using aiohttp's system.
        """|coro|

        Returns the users that reacted with this emoji.

        Parameters
        ----------
        emoji: :class:`str`
            Emoji to get users for.
        after: :class:`~pincer.utils.snowflake.Snowflake`
            Get users after this user ID. Returns all users if not provided.
            |default| ``0``
        limit: :class:`int`
            Max number of users to return (1-100).
            |default| ``25``
        """

        for user in await self._http.get(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
            f"?after={after}&limit={limit}"
        ):
            yield User.from_dict(user)

    async def remove_all_reactions(self):
        """|coro|

        Delete all reactions on a message. Requires the ``MANAGE_MESSAGES``
        intent.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions"
        )

    async def remove_emoji(self, emoji):
        """|coro|

        Deletes all the reactions for a given emoji on a message. Requires the
        ``MANAGE_MESSAGES`` intent.

        Parameters
        ----------
        emoji: :class:`str`
            Character for emoji. Does not need to be URL encoded.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
        )

    # TODO: Implement file (https://discord.com/developers/docs/resources/channel#edit-message)
    async def edit(
        self,
        content: str = None,
        embeds: List[Embed] = None,
        flags: int = None,
        allowed_mentions: AllowedMentions = None,
        attachments: List[Attachment] = None,
        components: List[MessageComponent] = None
    ):
        """|coro|

        Edit a previously sent message. The fields content, embeds, and flags
        can be edited by the original message author. Other users can only
        edit flags and only if they have the ``MANAGE_MESSAGES`` permission in
        the corresponding channel. When specifying flags, ensure to include
        all previously set flags/bits in addition to ones that you are
        modifying.

        Parameters
        ----------
        content: :class:`str`
            The message contents (up to 2000 characters)
            |default| ``None``
        embeds: List[:class:`~pincer.objects.message.embed.Embed`]
            Embedded rich content (up to 6000 characters)
        flags: :class:`int`
            Edit the flags of a message (only ``SUPPRESS_EMBEDS`` can
            currently be set/unset)
        allowed_mentions: :class:`~pincer.objects.message.message.AllowedMentions`
            allowed mentions for the message
        attachments: List[:class:`~pincer.objects.message.attachment.Attachment`]
            attached files to keep
        components: List[:class:`~pincer.objects.message.component.MessageComponent`]
            the components to include with the message
        """

        data = {}

        def set_if_not_none(value: Any, name: str):
            if isinstance(value, APIObject):
                data[name] = value.to_dict()
            elif value is not None:
                data[name] = value

        set_if_not_none(content, "content")
        set_if_not_none(embeds, "embeds")
        set_if_not_none(flags, "flags")
        set_if_not_none(allowed_mentions, "allowed_mentions")
        set_if_not_none(attachments, "attachments")
        set_if_not_none(components, "components")

        await self._http.patch(
            f"/channels/{self.channel_id}/messages/{self.id}",
            data=data
        )

    async def delete(self):
        """|coro|

        Delete a message. Requires the ``MANAGE_MESSAGES`` intent if the
        message was not sent by the current user.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}"
        )
