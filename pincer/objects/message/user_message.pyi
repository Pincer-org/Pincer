from ... import Client as Client
from ..._config import GatewayConfig as GatewayConfig
from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.conversion import construct_client_dict as construct_client_dict
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, JSONSerializable as JSONSerializable, MISSING as MISSING
from ..app.application import Application as Application
from ..app.interaction_base import MessageInteraction as MessageInteraction
from ..guild.channel import Channel as Channel, ChannelMention as ChannelMention
from ..guild.member import GuildMember as GuildMember
from ..guild.role import Role as Role
from ..user.user import User as User
from .attachment import Attachment as Attachment
from .component import MessageComponent as MessageComponent
from .embed import Embed as Embed
from .reaction import Reaction as Reaction
from .reference import MessageReference as MessageReference
from .sticker import StickerItem as StickerItem
from enum import Enum, IntEnum
from typing import Any, Generator, List, Optional, Union

class AllowedMentionTypes(str, Enum):
    ROLES: str
    USERS: str
    EVERYONE: str

class AllowedMentions(APIObject):
    parse: List[AllowedMentionTypes]
    roles: List[Union[Role, Snowflake]]
    users: List[Union[User, Snowflake]]
    reply: bool
    def to_dict(self): ...

class MessageActivityType(IntEnum):
    JOIN: int
    SPECTATE: int
    LISTEN: int
    JOIN_REQUEST: int

class MessageFlags(IntEnum):
    CROSSPOSTED: Any
    IS_CROSSPOST: Any
    SUPPRESS_EMBEDS: Any
    SOURCE_MESSAGE_DELETED: Any
    URGENT: Any
    HAS_THREAD: Any
    EPHEMERAL: Any
    LOADING: Any

class MessageType(IntEnum):
    DEFAULT: int
    RECIPIENT_ADD: int
    RECIPIENT_REMOVE: int
    CALL: int
    CHANNEL_NAME_CHANGE: int
    CHANNEL_ICON_CHANGE: int
    CHANNEL_PINNED_MESSAGE: int
    GUILD_MEMBER_JOIN: int
    USER_PREMIUM_GUILD_SUBSCRIPTION: int
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1: int
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2: int
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3: int
    CHANNEL_FOLLOW_ADD: int
    GUILD_DISCOVERY_DISQUALIFIED: int
    GUILD_DISCOVERY_REQUALIFIED: int
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING: int
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING: int
    THREAD_CREATED: int
    REPLY: int
    APPLICATION_COMMAND: int
    THREAD_STARTER_MESSAGE: int
    GUILD_INVITE_REMINDER: int
    CONTEXT_MENU_COMMAND: int

class MessageActivity(APIObject):
    type: MessageActivityType
    party_id: APINullable[str]

class UserMessage(APIObject, GuildProperty, ChannelProperty):
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
    edited_timestamp: APINullable[Timestamp]
    mention_channels: APINullable[List[ChannelMention]]
    guild_id: APINullable[Snowflake]
    member: APINullable[GuildMember]
    reactions: APINullable[List[Reaction]]
    nonce: APINullable[Union[int, str]]
    webhook_id: APINullable[Snowflake]
    activity: APINullable[MessageActivity]
    application: APINullable[Application]
    application_id: APINullable[Snowflake]
    message_reference: APINullable[MessageReference]
    flags: APINullable[MessageFlags]
    referenced_message: APINullable[Optional[UserMessage]]
    interaction: APINullable[MessageInteraction]
    thread: APINullable[Channel]
    components: APINullable[List[MessageComponent]]
    sticker_items: APINullable[List[StickerItem]]
    @classmethod
    async def from_id(cls, client: Client, _id: Snowflake, channel_id: Snowflake) -> UserMessage: ...
    async def get_most_recent(self): ...
    async def react(self, emoji: str): ...
    async def unreact(self, emoji: str): ...
    async def remove_user_reaction(self, emoji: str, user_id: Snowflake): ...
    async def get_reactions(self, emoji: str, after: Snowflake = ..., limit: int = ...) -> Generator[User, None, None]: ...
    async def remove_all_reactions(self) -> None: ...
    async def remove_emoji(self, emoji) -> None: ...
    async def edit(self, content: str = ..., embeds: List[Embed] = ..., flags: int = ..., allowed_mentions: AllowedMentions = ..., attachments: List[Attachment] = ..., components: List[MessageComponent] = ...): ...
    async def delete(self) -> None: ...
