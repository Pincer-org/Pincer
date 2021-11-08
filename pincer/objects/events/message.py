# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from typing import List

    from ..message.emoji import Emoji
    from ..guild.member import GuildMember
    from ...utils.snowflake import Snowflake


@dataclass
class MessageDeleteEvent(APIObject):
    """Sent when a message is deleted.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the message
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    guild_id: APIObject[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    """
    id: Snowflake
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageDeleteBulkEvent(APIObject):
    """Sent when multiple messages are deleted at once.

    Attributes
    ----------
    ids: List[:class:`~pincer.utils.snowflake.Snowflake`]
        The ids of the messages
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    guild_id: APIObject[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    """
    ids: List[Snowflake]
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionAddEvent(APIObject):
    """Sent when a user adds a reaction to a message.

    Attributes
    ----------
    user_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the user
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    message_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the message
    emoji: :class:`~pincer.objects.message.emoji.Emoji`
        The emoji used to react
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    member: :class:`~pincer.objects.guild.member.GuildMember`
        The member who reacted if this happened in a guild
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING


@dataclass
class MessageReactionRemoveEvent(APIObject):
    """Sent when a user removes a reaction from a message.

    Attributes
    ----------
    user_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the user
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    message_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the message
    emoji: :class:`~pincer.objects.message.emoji.Emoji`
        The emoji used to react
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveAllEvent(APIObject):
    """Sent when a user explicitly removes all reactions from a message.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    message_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the message
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    """
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveEmojiEvent(APIObject):
    """Sent when a bot removes all instances of a given
    emoji from the reactions of a message.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the channel
    message_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the message
    emoji: :class:`~pincer.objects.message.emoji.Emoji`
        The emoji that was removed
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild
    """
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
