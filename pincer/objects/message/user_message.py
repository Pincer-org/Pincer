# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum, Enum
from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.types import MISSING
from ..._config import GatewayConfig
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import List, Optional, Union

    from .embed import Embed
    from ..user.user import User
    from ..guild.role import Role
    from .reaction import Reaction
    from .sticker import StickerItem
    from .attachment import Attachment
    from ...utils.types import APINullable
    from ...utils.conversion import convert
    from .component import MessageComponent
    from .reference import MessageReference
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from ..app.application import Application
    from ..guild.channel import Channel, ChannelMention
    from ..app.interaction_base import MessageInteraction
    from ..guild.member import GuildMember, PartialGuildMember


class MessageActivityType(IntEnum):
    """The activity people can perform on a rich presence activity.

    Such an activity could for example be a spotify listen.

    Attributes
    ----------
    JOIN:
    SPECTATE:
    LISTEN:
    JOIN_REQUEST:
    """  # TODO docs: maybe do this, cba rn
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
    RECIPIENT_ADD:
    RECIPIENT_REMOVE:
    CALL:
    CHANNEL_NAME_CHANGE:
    CHANNEL_ICON_CHANGE:
    CHANNEL_PINNED_MESSAGE:
    GUILD_MEMBER_JOIN:
    USER_PREMIUM_GUILD_SUBSCRIPTION:
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1:
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2:
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3:
    CHANNEL_FOLLOW_ADD:
    GUILD_DISCOVERY_DISQUALIFIED:
    GUILD_DISCOVERY_REQUALIFIED:
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING:
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING:
    THREAD_CREATED:
    REPLY:
    APPLICATION_COMMAND:
    THREAD_STARTER_MESSAGE:
    GUILD_INVITE_REMINDER:
    """  # TODO docs: maybe do this too, really cba rn
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
    USERS = "user"
    EVERYONE = "everyone"


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
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: Timestamp
    edited_timestamp: Optional[Timestamp]
    tts: bool
    mention_everyone: bool
    mentions: List[GuildMember]
    mention_roles: List[Role]
    attachments: List[Attachment]
    embeds: List[Embed]
    pinned: bool
    type: MessageType

    mention_channels: APINullable[List[ChannelMention]] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[PartialGuildMember] = MISSING
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

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
        self.channel_id = convert(self.channel_id, Snowflake.from_string)
        self.author = convert(self.author, User.from_dict, client=self._client)
        self.timestamp = convert(self.timestamp, Timestamp)
        self.edited_timestamp = convert(self.edited_timestamp, Timestamp)
        self.mentions = convert(self.mentions, PartialGuildMember.from_dict,
                                client=self._client)
        self.mention_roles = convert(self.mention_roles, Role.from_dict)
        self.attachments = convert(self.attachments, Attachment.from_dict)
        self.embeds = convert(self.embeds, Embed.from_dict)
        self.mention_channels = convert(
            self.mention_channels,
            ChannelMention.from_dict
        )
        self.guild_id = convert(self.guild_id, Snowflake.from_string)
        self.member = convert(self.member, GuildMember.from_dict,
                              client=self._client)
        self.reactions = convert(self.reactions, Reaction.from_dict)
        self.webhook_id = convert(self.webhook_id, Snowflake.from_string)
        self.activity = convert(self.activity, MessageActivity.from_dict)
        self.application = convert(
            self.application, Application.from_dict)
        self.application_id = convert(
            self.application_id,
            Snowflake.from_string
        )
        self.message_reference = convert(
            self.message_reference,
            MessageReference.from_dict
        )
        # self.flags = convert(self.flags, MessageFlags.from_bytes)
        # self.referenced_message = convert(
        #     self.referenced_message,
        #     Message.from_dict
        # )
        self.interaction = convert(
            self.interaction,
            MessageInteraction.from_dict
        )
        self.thread = convert(self.thread, Channel.from_dict,
                              client=self._client)
        self.components = convert(self.components, MessageComponent.from_dict)
        self.sticker_items = convert(self.sticker_items, StickerItem.from_dict)
