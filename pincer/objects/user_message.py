# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import List, Optional, Union, TYPE_CHECKING


from .application import Application
from .attachment import Attachment
from .channel import Channel, ChannelMention
from .embed import Embed
from .guild_member import GuildMember
from .interaction_base import MessageInteraction
from .message_component import MessageComponent
from .message_reference import MessageReference
from .reaction import Reaction
from .role import Role
from .sticker import StickerItem
from .user import User
from ..core.http import HTTPClient
from .._config import GatewayConfig
from ..utils import APIObject, APINullable, MISSING, Snowflake, Timestamp, \
    convert

if TYPE_CHECKING:
    from .. import Client


class MessageActivityType(IntEnum):
    """
    The activity people can perform on a rich presence activity.

    Such an activity could for example be a spotify listen.
    """
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlags(IntEnum):
    """
    Special message properties.

    :param CROSSPOSTED:
        the message has been published to subscribed
        channels (via Channel Following)

    :param IS_CROSSPOST:
        this message originated from a message
        in another channel (via Channel Following)

    :param SUPPRESS_EMBEDS:
        do not include any embeds when serializing this message

    :param SOURCE_MESSAGE_DELETED:
        the source message for this crosspost
        has been deleted (via Channel Following)

    :param URGENT:
        this message came from the urgent message system

    :param HAS_THREAD:
        this message has an associated thread,
        with the same id as the message

    :param EPHEMERAL:
        this message is only visible to the user
        who invoked the Interaction

    :param LOADING:
        this message is an Interaction
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
    """
    Represents the type of the message.
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
    """
    Represents a Discord Message Activity object

    :param type:
        type of message activity

    :param party_id:
        party_id from a Rich Presence event
    """
    type: MessageActivityType
    party_id: APINullable[str] = MISSING


class AllowedMentionTypes(str, Enum):
    """
    The allowed mentions.

    :param ROLES:
        Controls role mentions

    :param USERS:
        Controls user mentions

    :param EVERYONE:
        Controls @everyone and @here mentions
    """
    ROLES = "roles"
    USERS = "user"
    EVERYONE = "everyone"


@dataclass
class UserMessage(APIObject):
    """
    Represents a message sent in a channel within Discord.

    :param _client:

    :param _http:

    :param id:
        id of the message

    :param channel_id:
        id of the channel the message was sent in

    :param guild_id:
        id of the guild the message was sent in

    :param author:
        the author of this message (not guaranteed to be a valid user)

    :param member:
        member properties for this message's author

    :param content:
        contents of the message

    :param timestamp:
        when this message was sent

    :param edited_timestamp:
        when this message was edited (or null if never)

    :param tts:
        whether this was a TTS message

    :param mention_everyone:
        whether this message mentions everyone

    :param mentions:
        users specifically mentioned in the message

    :param mention_roles:
        roles specifically mentioned in this message

    :param mention_channels:
        channels specifically mentioned in this message

    :param attachments:
        any attached files

    :param embeds:
        any embedded content

    :param reactions:
        reactions to the message

    :param nonce:
        user for validating a message was sent

    :param pinned:
        whether this message is pinned

    :param webhook_id:
        if the message is generated by a webhook,
        this is the webhook's id

    :param type:
        type of message

    :param activity:
        sent with Rich Presence-related chat embeds

    :param application:
        sent with Rich Presence-related chat embeds

    :param application_id:
        if the message is a response to an Interaction,
        this is the id of the interaction's application

    :param message_reference:
        data showing the source of a crosspost,
        channel follow add, pin, or reply message

    :param flags:
        message flags combined as a bitfield

    :param referenced_message:
        the message associated with the message_reference

    :param interaction:
        sent if the message is a response to an Interaction

    :param thread:
        the thread that was started from this message,
        includes thread member object

    :param components:
        sent if the message contains components like buttons,
        action rows, or other interactive components

    :param sticker_items:
        sent if the message contains stickers
    """
    _client: Client
    _http: HTTPClient

    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: Timestamp
    edited_timestamp: Optional[Timestamp]
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Role]
    attachments: List[Attachment]
    embeds: List[Embed]
    pinned: bool
    type: MessageType

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
    referenced_message: APINullable[Optional[Message]] = MISSING
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
        self.mentions = convert(self.mentions, User.from_dict, client=self._client)
        self.mention_roles = convert(self.mention_roles, Role.from_dict)
        self.attachments = convert(self.attachments, Attachment.from_dict)
        self.embeds = convert(self.embeds, Embed.from_dict)
        self.mention_channels = convert(
            self.mention_channels,
            ChannelMention.from_dict
        )
        self.guild_id = convert(self.guild_id, Snowflake.from_string)
        self.member = convert(self.member, GuildMember.from_dict, client=self._client)
        self.reactions = convert(self.reactions, Reaction.from_dict)
        self.webhook_id = convert(self.webhook_id, Snowflake.from_string)
        self.activity = convert(self.activity, MessageActivity.from_dict)
        self.application = convert(self.application, Application.from_dict)
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
        self.thread = convert(self.thread, Channel.from_dict, client=self._client)
        self.components = convert(self.components, MessageComponent.from_dict)
        self.sticker_items = convert(self.sticker_items, StickerItem.from_dict)
