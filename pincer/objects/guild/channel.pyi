from ..._config import GatewayConfig as GatewayConfig
from ...client import Client as Client
from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.conversion import construct_client_dict as construct_client_dict, remove_none as remove_none
from ...utils.convert_message import convert_message as convert_message
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..message.embed import Embed as Embed
from ..message.message import Message as Message
from ..message.user_message import UserMessage as UserMessage
from ..user.user import User as User
from .invite import Invite as Invite, InviteTargetType as InviteTargetType
from .member import GuildMember as GuildMember
from .overwrite import Overwrite as Overwrite
from .thread import ThreadMetadata as ThreadMetadata
from .webhook import Webhook as Webhook
from enum import IntEnum
from typing import AsyncGenerator, AsyncIterator, List, Optional, Union, overload

class ChannelType(IntEnum):
    GUILD_TEXT: int
    DM: int
    GUILD_VOICE: int
    GROUP_DM: int
    GUILD_CATEGORY: int
    GUILD_NEWS: int
    GUILD_STORE: int
    GUILD_NEWS_THREAD: int
    GUILD_PUBLIC_THREAD: int
    GUILD_PRIVATE_THREAD: int
    GUILD_STAGE_VOICE: int

class Channel(APIObject, GuildProperty):
    id: Snowflake
    type: ChannelType
    application_id: APINullable[Snowflake]
    bitrate: APINullable[int]
    default_auto_archive_duration: APINullable[int]
    guild_id: APINullable[Snowflake]
    icon: APINullable[Optional[str]]
    last_message_id: APINullable[Optional[Snowflake]]
    last_pin_timestamp: APINullable[Optional[Timestamp]]
    member: APINullable[GuildMember]
    member_count: APINullable[int]
    message_count: APINullable[int]
    name: APINullable[str]
    nsfw: APINullable[bool]
    owner_id: APINullable[Snowflake]
    parent_id: APINullable[Optional[Snowflake]]
    permissions: APINullable[str]
    permission_overwrites: APINullable[List[Overwrite]]
    position: APINullable[int]
    rate_limit_per_user: APINullable[int]
    recipients: APINullable[List[User]]
    rtc_region: APINullable[Optional[str]]
    thread_metadata: APINullable[ThreadMetadata]
    topic: APINullable[Optional[str]]
    user_limit: APINullable[int]
    video_quality_mode: APINullable[int]
    @property
    def mention(self): ...
    @classmethod
    async def from_id(cls, client: Client, channel_id: int) -> Channel: ...
    @overload
    async def edit(self, *, name: str = ..., type: ChannelType = ..., position: int = ..., topic: str = ..., nsfw: bool = ..., rate_limit_per_user: int = ..., bitrate: int = ..., user_limit: int = ..., permissions_overwrites: List[Overwrite] = ..., parent_id: Snowflake = ..., rtc_region: str = ..., video_quality_mod: int = ..., default_auto_archive_duration: int = ...) -> Channel: ...
    async def edit_permissions(self, overwrite: Overwrite, allow: str, deny: str, type: int, reason: Optional[str] = ...): ...
    async def delete_permission(self, overwrite: Overwrite, reason: Optional[str] = ...): ...
    async def follow_news_channel(self, webhook_channel_id: Snowflake) -> NewsChannel: ...
    async def trigger_typing_indicator(self) -> None: ...
    async def get_pinned_messages(self) -> AsyncIterator[UserMessage]: ...
    async def pin_message(self, message: UserMessage, reason: Optional[str] = ...): ...
    async def unpin_message(self, message: UserMessage, reason: Optional[str] = ...): ...
    async def group_dm_add_recipient(self, user: User, access_token: Optional[str] = ..., nick: Optional[str] = ...): ...
    async def group_dm_remove_recipient(self, user: User): ...
    async def bulk_delete_messages(self, messages: List[Snowflake], reason: Optional[str] = ...): ...
    async def delete(self, reason: Optional[str] = ..., channel_id: Optional[Snowflake] = ...): ...
    async def send(self, message: Union[Embed, Message, str]) -> UserMessage: ...
    async def get_webhooks(self) -> AsyncGenerator[Webhook, None]: ...
    async def get_invites(self) -> AsyncIterator[Invite]: ...
    async def create_invite(self, max_age: int = ..., max_uses: int = ..., temporary: bool = ..., unique: bool = ..., target_type: InviteTargetType = ..., target_user_id: Snowflake = ..., target_application_id: Snowflake = ..., reason: Optional[str] = ...): ...

class TextChannel(Channel):
    @overload
    async def edit(self, name: str = ..., type: ChannelType = ..., position: int = ..., topic: str = ..., nsfw: bool = ..., rate_limit_per_user: int = ..., permissions_overwrites: List[Overwrite] = ..., parent_id: Snowflake = ..., default_auto_archive_duration: int = ...) -> Union[TextChannel, NewsChannel]: ...
    async def fetch_message(self, message_id: int) -> UserMessage: ...

class VoiceChannel(Channel):
    @overload
    async def edit(self, name: str = ..., position: int = ..., bitrate: int = ..., user_limit: int = ..., permissions_overwrites: List[Overwrite] = ..., rtc_region: str = ..., video_quality_mod: int = ...) -> VoiceChannel: ...

class GroupDMChannel(Channel): ...
class CategoryChannel(Channel): ...

class NewsChannel(Channel):
    @overload
    async def edit(self, name: str = ..., type: ChannelType = ..., position: int = ..., topic: str = ..., nsfw: bool = ..., permissions_overwrites: List[Overwrite] = ..., parent_id: Snowflake = ..., default_auto_archive_duration: int = ...) -> Union[TextChannel, NewsChannel]: ...

class PublicThread(Channel): ...
class PrivateThread(Channel): ...

class ChannelMention(APIObject):
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str
