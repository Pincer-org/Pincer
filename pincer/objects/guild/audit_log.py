# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Optional, List, TYPE_CHECKING

from ...utils.types import MISSING
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Any, List, Optional

    from ..user.user import User
    from ..guild.channel import Channel
    from ..guild.webhook import Webhook
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ..user.integration import Integration


class AuditLogEvent(IntEnum):
    """Audit log action type.
    This represents the action which got performed,
    and logged.
    """
    GUILD_UPDATE = 1  #: Guild updated
    CHANNEL_CREATE = 10  #: Channel created
    CHANNEL_UPDATE = 11  #: Channel updated
    CHANNEL_DELETE = 12  #: Channel deleted
    CHANNEL_OVERWRITE_CREATE = 13  #: Channel overwrites created
    CHANNEL_OVERWRITE_UPDATE = 14  #: Channel overwrites updated
    CHANNEL_OVERWRITE_DELETE = 15  #: Channel overwrites deleted
    MEMBER_KICK = 20  #: Member kicked
    MEMBER_PRUNE = 21  #: Members pruned
    MEMBER_BAN_ADD = 22  #: Member banned
    MEMBER_BAN_REMOVE = 23  #: Member unbanned
    MEMBER_UPDATE = 24  #: Member edit
    MEMBER_ROLE_UPDATE = 25  #: Member role change
    MEMBER_MOVE = 26  #: Member voice channel move
    MEMBER_DISCONNECT = 27  #: Member voice channel disconnect
    BOT_ADD = 28  #: Bot added
    ROLE_CREATE = 30  #: Role created
    ROLE_UPDATE = 31  #: Role updated
    ROLE_DELETE = 32  #: Role deleted
    INVITE_CREATE = 40  #: Invite created
    INVITE_UPDATE = 41  #: Invite updated
    INVITE_DELETE = 42  #: Invite deleted
    WEBHOOK_CREATE = 50  #: Webhook created
    WEBHOOK_UPDATE = 51  #: Webhook updated
    WEBHOOK_DELETE = 52  #: Webhook deleted
    EMOJI_CREATE = 60  #: Emoji created
    EMOJI_UPDATE = 61  #: Emoji updated
    EMOJI_DELETE = 62  #: Emoji deleted
    MESSAGE_DELETE = 72  #: Message deleted
    MESSAGE_BULK_DELETE = 73  #: Messave bulk delete
    MESSAGE_PIN = 74  #: Message pinned
    MESSAGE_UNPIN = 75  #: Message unpinned
    INTEGRATION_CREATE = 80  #: Integration created
    INTEGRATION_UPDATE = 81  #: Integration updated
    INTEGRATION_DELETE = 82  #: Integration deleted
    STAGE_INSTANCE_CREATE = 83  #: Stage instance created
    STAGE_INSTANCE_UPDATE = 84  #: Stage instance updated
    STAGE_INSTANCE_DELETE = 85  #: Stage instance deleted
    STICKER_CREATE = 90  #: Sticker created
    STICKER_UPDATE = 91  #: Sticker updated
    STICKER_DELETE = 92  #: Sticker deleted
    THREAD_CREATE = 110  #: Thread created
    THREAD_UPDATE = 111  #: Thread updated
    THREAD_DELETE = 112  #: Thread deleted


@dataclass
class AuditLogChange(APIObject):
    """Representation of Discord Audit Log Change object

    Attributes
    ----------
    new_value: Any
        New value of the key
    old_value: Any
        Old value of the key
    key: :class:`str`
        Name of audit log change key
    """
    new_value: Any
    old_value: Any
    key: str


@dataclass
class AuditEntryInfo(APIObject):
    """Represents Discord Optional Audit Entry Info

    Attributes
    ----------
    delete_member_days: :class:`str`
        Number of days after which inactive members were kicked
    members_removed: :class:`str`
        Number of members removed by the prune
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Channel in which the entities were targeted
    message_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the message that was targeted
    count: :class:`str`
        Number of entities that were targeted
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the overwritten entity
    type: :class:`str`
        Type of overwritten entity - "0" for "role" or "1" for "member"
    role_name: :class:`str`
        Name of the role if type is "0" (not present if type is "1")
    """
    delete_member_days: str
    members_removed: str
    channel_id: Snowflake
    message_id: Snowflake
    count: str
    id: Snowflake
    type: str
    role_name: str


@dataclass
class AuditLogEntry(APIObject):
    """Represents a Discord Audit Log Entry object.

    Attributes
    ----------
    target_id: Optional[:class:`str`]
        Id of the affected entity x(webhook, user, role, etc.)
    user_id: :class:`~pincer.utils.snowflake.Snowflake`
        The user who made the changes
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the entry
    action_type: :class:`~pincer.objects.guild.audit_log.AuditLogEvent`
        Type of action that occurred
    changes: APINullable[List[:class:`~pincer.objects.guild.audit_log.AuditLogChange`]]
        Changes made to the target_id
    options: APINullable[List[:class:`~pincer.objects.guild.audit_log.AuditLogChange`]]
        Additional info for certain action types
    reason: APINullable[:class:`str`]
        The reason for the change x(0-512 characters)
    """
    target_id: Optional[str]
    user_id: Optional[Snowflake]
    id: Snowflake
    action_type: AuditLogEvent

    changes: APINullable[List[AuditLogChange]] = MISSING
    options: APINullable[AuditEntryInfo] = MISSING
    reason: APINullable[str] = MISSING


@dataclass
class AuditLog(APIObject):
    """Represents a Discord Audit Log object.

    webhooks: List[:class:`~pincer.objects.guild.webhook.Webhook`]
        list of webhooks found in the audit log
    users: List[:class:`~pincer.objects.user.user.User`]
        list of users found in the audit log
    audit_log_entries: List[:class:`~pincer.objects.guild.audit_log.AuditLogEntry`]
        list of audit log entries
    integrations: List[:class:`~pincer.objects.user.integration.Integration`]
        list of partial integration objects
    threads: List[:class:`~pincer.objects.guild.channel.Channel`]
        list of threads found in the audit log
    """
    webhooks: List[Webhook]
    users: List[User]
    audit_log_entries: List[AuditLogEntry]
    integrations: List[Integration]
    threads: List[Channel]
