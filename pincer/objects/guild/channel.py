# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, Optional, List, TYPE_CHECKING, Union, overload

from ..._config import GatewayConfig
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..guild.overwrite import Overwrite
    from ..guild.thread import ThreadMetadata
    from ..guild.member import GuildMember
    from ..user import User
    from ... import Client
    from ...core.http import HTTPClient
    from ...utils import APINullable, Snowflake, Timestamp


class ChannelType(IntEnum):
    """Represents a channel its type."""
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6

    if GatewayConfig.version >= 9:
        GUILD_NEWS_THREAD = 10
        GUILD_PUBLIC_THREAD = 11
        GUILD_PRIVATE_THREAD = 12

    GUILD_STAGE_VOICE = 13


@dataclass
class Channel(APIObject):
    """
    Represents a Discord Channel Mention object

    :param _client:
        reference to the Client

    :param _http:
        reference to the HTTPClient

    :param id:
        the id of this channel

    :param type:
        the type of channel

    :param application_id:
        application id of the group DM creator if it is bot-created

    :param bitrate:
        the bitrate (in bits) of the voice channel

    :param default_auto_archive_duration:
        default duration for newly created threads, in minutes, to
        automatically archive the thread after recent activity, can be set to:
        60, 1440, 4320, 10080

    :param guild_id:
        the id of the guild (may be missing for some channel objects received
        over gateway guild dispatches)

    :param icon:
        icon hash
    :param last_message_id:
        the id of the last message sent in this channel (may not point to an
        existing or valid message)

    :param last_pin_timestamp:
        when the last pinned message was pinned. This may be null in events
        such as GUILD_CREATE when a message is not pinned.

    :param member:
        thread member object for the current user, if they have joined the
        thread, only included on certain API endpoints

    :param member_count:
        an approximate count of users in a thread, stops counting at 50

    :param message_count:
        an approximate count of messages in a thread, stops counting at 50

    :param name:
        the name of the channel (1-100 characters)

    :param nsfw:
        whether the channel is nsfw

    :param owner_id:
        id of the creator of the group DM or thread

    :param parent_id:
        for guild channels: id of the parent category for a channel (each
        parent category can contain up to 50 channels), for threads: id of the
        text channel this thread was created

    :param permissions:
        computed permissions for the invoking user in the channel, including
        overwrites, only included when part of the resolved data received on a
        slash command interaction

    :param permission_overwrites:
        explicit permission overwrites for members and roles

    :param position:
        sorting position of the channel

    :param rate_limit_per_user:
        amount of seconds a user has to wait before sending another message
        (0-21600); bots, as well as users with the permission manage_messages
        or manage_channel, are unaffected

    :param recipients:
        the recipients of the DM

    :param rtc_region:
        voice region id for the voice channel, automatic when set to null

    :param thread_metadata:
        thread-specific fields not needed by other channels

    :param topic:
        the channel topic (0-1024 characters)

    :param user_limit:
        the user limit of the voice channel

    :param video_quality_mode:
        the camera video quality mode of the voice channel, 1 when not present
    """

    _client: Client
    _http: HTTPClient

    id: Snowflake
    type: ChannelType

    application_id: APINullable[Snowflake] = MISSING
    bitrate: APINullable[int] = MISSING
    default_auto_archive_duration: APINullable[int] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    icon: APINullable[Optional[str]] = MISSING

    last_message_id: APINullable[Optional[Snowflake]] = MISSING
    last_pin_timestamp: APINullable[Optional[Timestamp]] = MISSING
    member: APINullable[GuildMember] = MISSING

    member_count: APINullable[int] = MISSING

    message_count: APINullable[int] = MISSING

    name: APINullable[str] = MISSING
    nsfw: APINullable[bool] = MISSING
    owner_id: APINullable[Snowflake] = MISSING
    parent_id: APINullable[Optional[Snowflake]] = MISSING
    permissions: APINullable[str] = MISSING
    permission_overwrites: APINullable[List[Overwrite]] = MISSING
    position: APINullable[int] = MISSING
    rate_limit_per_user: APINullable[int] = MISSING
    recipients: APINullable[List[User]] = MISSING
    rtc_region: APINullable[Optional[str]] = MISSING
    thread_metadata: APINullable[ThreadMetadata] = MISSING
    topic: APINullable[Optional[str]] = MISSING
    user_limit: APINullable[int] = MISSING
    video_quality_mode: APINullable[int] = MISSING

    @classmethod
    async def from_id(cls, client: Client, id: int) -> Channel:
        data = (await client.http.get(f"channels/{id}")) or {}
        data.update(
            {
                "_client": client,
                "_http": client.http,
                "type": ChannelType(data.pop("type"))
            }
        )

        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)

    @overload
    async def edit(
            self, *, name: str = None,
            type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            rate_limit_per_user: int = None, bitrate: int = None,
            user_limit: int = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None, rtc_region: str = None,
            video_quality_mod: int = None,
            default_auto_archive_duration: int = None
    ) -> Channel:
        ...

    async def edit(self, **kwargs):
        data = await self._http.patch(f"channels/{self.id}", kwargs)
        data.update(
            {
                "_client": self.client,
                "_http": self._http,
                "type": ChannelType(data.pop("type"))
            }
        )
        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)


def __str__(self):
    """return the discord tag when object gets used as a string."""
    return self.name or str(self.id)


class TextChannel(Channel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            rate_limit_per_user: int = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None,
            default_auto_archive_duration: int = None
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        return await super().edit(**kwargs)


class VoiceChannel(Channel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, position: int = None, bitrate: int = None,
            user_limit: int = None,
            permissions_overwrites: List[Overwrite] = None,
            rtc_region: str = None, video_quality_mod: int = None
    ) -> VoiceChannel:
        ...

    async def edit(self, **kwargs):
        return await super().edit(**kwargs)


class CategoryChannel(Channel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewsChannel(Channel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None,
            default_auto_archive_duration: int = None
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        return await super().edit(**kwargs)


@dataclass
class ChannelMention(APIObject):
    """
    Represents a Discord Channel Mention object

    :param id:
        id of the channel

    :param guild_id:
        id of the guild containing the channel

    :param type:
        the type of channel

    :param name:
        the name of the channel
    """
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


_channel_type_map: Dict[ChannelType, Channel] = {
    ChannelType.GUILD_TEXT: TextChannel,
    ChannelType.GUILD_VOICE: VoiceChannel,
    ChannelType.GUILD_CATEGORY: CategoryChannel,
    ChannelType.GUILD_NEWS: NewsChannel
}
