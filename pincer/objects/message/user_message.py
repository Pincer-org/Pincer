# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import Any, Generator, List, Optional, Union, TYPE_CHECKING

from ..._config import GatewayConfig
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..app.application import Application
    from ..app.interaction_base import MessageInteraction
    from ..guild.channel import Channel, ChannelMention
    from ..guild.member import GuildMember
    from ..guild.role import Role
    from ..message.attachment import Attachment
    from ..message.component import MessageComponent
    from ..message.embed import Embed
    from ..message.reaction import Reaction
    from ..message.reference import MessageReference
    from ..message.sticker import StickerItem
    from ..user import User
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from ...utils import APINullable


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
    USERS = "users"
    EVERYONE = "everyone"


@dataclass
class AllowedMentions(APIObject):
    parse: List[AllowedMentionTypes]
    roles: List[Union[Role, Snowflake]]
    users: List[Union[User, Snowflake]]
    reply: bool = True

    @staticmethod
    def get_str_id(obj: Union[Snowflake, User, Role]) -> str:
        if hasattr(obj, "id"):
            obj = obj.id

        return str(obj)

    def to_dict(self):
        return {
            "parse": self.parse,
            "roles": list(map(self.get_str_id, self.roles)),
            "users": list(map(self.get_str_id, self.users)),
            "replied_user": self.reply
        }


@dataclass
class UserMessage(APIObject):
    """
    Represents a message sent in a channel within Discord.

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
        """
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
        """
        Create a reaction for the message. Requires the
        ``READ_MESSAGE_HISTORY` itent. ``ADD_REACTIONS`` intent is required if
        nobody else has reacted using the emoji.

        :param emoji:
            Character for emoji. Does not need to be URL encoded.
        """

        await self._http.put(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
        )

    async def unreact(self, emoji: str):
        """
        Delete a reaction the current user has made for the message.

        :param emoji:
            Character for emoji. Does not need to be URL encoded.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
        )

    async def remove_user_reaction(self, emoji: str, user_id: Snowflake):
        """
        Deletes another user's reaction. Requires the ``MANAGE_MESSAGES``
        intent.

        :param emoji:
            Character for emoji. Does not need to be URL encoded.

        :param user_id:
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
        """
        Returns the users that reacted with this emoji.

        :param after:
            Get users after this user ID. Returns all users if not provided.

        :param limit:
            Max number of users to return (1-100). 25 if not provided.
        """

        for user in await self._http.get(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
            f"?after={after}&limit={limit}"
        ):
            yield User.from_dict(user)

    async def remove_all_reactions(self):
        """
        Delete all reactions on a message. Requires the ``MANAGE_MESSAGES``
        intent.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}/reactions"
        )

    async def remove_emoji(self, emoji):
        """
        Deletes all the reactions for a given emoji on a message. Requires the
        ``MANAGE_MESSAGES`` intent.

        :param emoji:
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
        """
        Edit a previously sent message. The fields content, embeds, and flags
        can be edited by the original message author. Other users can only
        edit flags and only if they have the ``MANAGE_MESSAGES`` permission in
        the corresponding channel. When specifying flags, ensure to include
        all previously set flags/bits in addition to ones that you are
        modifying.

        :param content:
            The message contents (up to 2000 characters)

        :param embeds:
            Embedded rich content (up to 6000 characters)

        :param flags:
            Edit the flags of a message (only ``SUPPRESS_EMBEDS`` can
            currently be set/unset)

        :param allowed_mentions:
            allowed mentions for the message

        :param attachments:
            attached files to keep

        :param components:
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
        """
        Delete a message. Requires the ``MANAGE_MESSAGES`` intent if the
        message was not sent by the current user.
        """

        await self._http.delete(
            f"/channels/{self.channel_id}/messages/{self.id}"
        )
