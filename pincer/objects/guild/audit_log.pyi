from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.channel import Channel as Channel
from ..guild.webhook import Webhook as Webhook
from ..user.integration import Integration as Integration
from ..user.user import User as User
from enum import IntEnum
from typing import Any, List, Optional

class AuditLogEvent(IntEnum):
    GUILD_UPDATE: int
    CHANNEL_CREATE: int
    CHANNEL_UPDATE: int
    CHANNEL_DELETE: int
    CHANNEL_OVERWRITE_CREATE: int
    CHANNEL_OVERWRITE_UPDATE: int
    CHANNEL_OVERWRITE_DELETE: int
    MEMBER_KICK: int
    MEMBER_PRUNE: int
    MEMBER_BAN_ADD: int
    MEMBER_BAN_REMOVE: int
    MEMBER_UPDATE: int
    MEMBER_ROLE_UPDATE: int
    MEMBER_MOVE: int
    MEMBER_DISCONNECT: int
    BOT_ADD: int
    ROLE_CREATE: int
    ROLE_UPDATE: int
    ROLE_DELETE: int
    INVITE_CREATE: int
    INVITE_UPDATE: int
    INVITE_DELETE: int
    WEBHOOK_CREATE: int
    WEBHOOK_UPDATE: int
    WEBHOOK_DELETE: int
    EMOJI_CREATE: int
    EMOJI_UPDATE: int
    EMOJI_DELETE: int
    MESSAGE_DELETE: int
    MESSAGE_BULK_DELETE: int
    MESSAGE_PIN: int
    MESSAGE_UNPIN: int
    INTEGRATION_CREATE: int
    INTEGRATION_UPDATE: int
    INTEGRATION_DELETE: int
    STAGE_INSTANCE_CREATE: int
    STAGE_INSTANCE_UPDATE: int
    STAGE_INSTANCE_DELETE: int
    STICKER_CREATE: int
    STICKER_UPDATE: int
    STICKER_DELETE: int
    THREAD_CREATE: int
    THREAD_UPDATE: int
    THREAD_DELETE: int

class AuditLogChange(APIObject):
    new_value: Any
    old_value: Any
    key: str

class AuditEntryInfo(APIObject, ChannelProperty):
    delete_member_days: str
    members_removed: str
    channel_id: Snowflake
    message_id: Snowflake
    count: str
    id: Snowflake
    type: str
    role_name: str

class AuditLogEntry(APIObject):
    target_id: Optional[str]
    user_id: Optional[Snowflake]
    id: Snowflake
    action_type: AuditLogEvent
    changes: APINullable[List[AuditLogChange]]
    options: APINullable[AuditEntryInfo]
    reason: APINullable[str]

class AuditLog(APIObject):
    webhooks: List[Webhook]
    users: List[User]
    audit_log_entries: List[AuditLogEntry]
    integrations: List[Integration]
    threads: List[Channel]
