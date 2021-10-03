# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import List

from ..guild.member import GuildMember
from ..message.emoji import Emoji
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.types import APINullable, MISSING


@dataclass
class MessageDeleteEvent(APIObject):
    """
    Sent when a message is deleted.

    :param id:
        the id of the message

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild
    """
    id: Snowflake
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageDeleteBulkEvent(APIObject):
    """
    Sent when multiple messages are deleted at once.

    :param ids:
        the ids of the messages

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild
    """
    ids: List[Snowflake]
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionAddEvent(APIObject):
    """
    Sent when a user adds a reaction to a message.

    :param user_id:
        the id of the user

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild

    :param member:
        the member who reacted if this happened in a guild

    :param emoji:
        the emoji used to react
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING


@dataclass
class MessageReactionRemoveEvent(APIObject):
    """
    Sent when a user removes a reaction from a message.

    :param user_id:
        the id of the user

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild

    :param emoji:
        the emoji used to react
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveAllEvent(APIObject):
    """
    Sent when a user explicitly removes all reactions from a message.

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild
    """
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveEmojiEvent(APIObject):
    """
    Sent when a bot removes all instances of a given
    emoji from the reactions of a message.

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild

    :param message_id:
        the id of the message

    :param emoji:
        the emoji that was removed
    """
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
