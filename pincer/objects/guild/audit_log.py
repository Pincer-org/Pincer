# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Any, List, Optional

    from ...utils.snowflake import Snowflake
    from ...utils.types import APINullable
    from ..guild.channel import Channel
    from ..guild.webhook import Webhook
    from ..user.integration import Integration
    from ..user.user import User


class AuditLogEvent(IntEnum):
    """Audit log action type.
    This represents the action which got performed,
    and logged.

    Attributes
    ----------
    GUILD_UPDATE:
        Guild updated.
    CHANNEL_CREATE:
        Channel created.
    CHANNEL_UPDATE:
        Channel updated.
    CHANNEL_DELETE:
        Channel deleted.
    CHANNEL_OVERWRITE_CREATE:
        Channel overwrites created.
    CHANNEL_OVERWRITE_UPDATE:
        Channel overwrites updated.
    CHANNEL_OVERWRITE_DELETE:
        Channel overwrites deleted.
    MEMBER_KICK:
        Member kicked.
    MEMBER_PRUNE:
        Members pruned.
    MEMBER_BAN_ADD:
        Member banned.
    MEMBER_BAN_REMOVE:
        Member unbanned.
    MEMBER_UPDATE:
        Member edit.
    MEMBER_ROLE_UPDATE:
        Member role change.
    MEMBER_MOVE:
        Member voice channel move.
    MEMBER_DISCONNECT:
        Member voice channel disconnect.
    BOT_ADD:
        Bot added.
    ROLE_CREATE:
        Role created.
    ROLE_UPDATE:
        Role updated.
    ROLE_DELETE:
        Role deleted.
    INVITE_CREATE:
        Invite created.
    INVITE_UPDATE:
        Invite updated.
    INVITE_DELETE:
        Invite deleted.
    WEBHOOK_CREATE:
        Webhook created.
    WEBHOOK_UPDATE:
        Webhook updated.
    WEBHOOK_DELETE:
        Webhook deleted.
    EMOJI_CREATE:
        Emoji created.
    EMOJI_UPDATE:
        Emoji updated.
    EMOJI_DELETE:
        Emoji deleted.
    MESSAGE_DELETE:
        Message deleted.
    MESSAGE_BULK_DELETE:
        Message bulk delete.
    MESSAGE_PIN:
        Message pinned.
    MESSAGE_UNPIN:
        Message unpinned.
    INTEGRATION_CREATE:
        Integration created.
    INTEGRATION_UPDATE:
        Integration updated.
    INTEGRATION_DELETE:
        Integration deleted.
    STAGE_INSTANCE_CREATE:
        Stage instance created.
    STAGE_INSTANCE_UPDATE:
        Stage instance updated.
    STAGE_INSTANCE_DELETE:
        Stage instance deleted.
    STICKER_CREATE:
        Sticker created.
    STICKER_UPDATE:
        Sticker updated.
    STICKER_DELETE:
        Sticker deleted.
    THREAD_CREATE1:
        Thread created.
    THREAD_UPDATE1:
        Thread updated.
    THREAD_DELETE1:
        Thread deleted.
    """
    GUILD_UPDATE = 1
    CHANNEL_CREATE = 10
    CHANNEL_UPDATE = 11
    CHANNEL_DELETE = 12
    CHANNEL_OVERWRITE_CREATE = 13
    CHANNEL_OVERWRITE_UPDATE = 14
    CHANNEL_OVERWRITE_DELETE = 15
    MEMBER_KICK = 20
    MEMBER_PRUNE = 21
    MEMBER_BAN_ADD = 22
    MEMBER_BAN_REMOVE = 23
    MEMBER_UPDATE = 24
    MEMBER_ROLE_UPDATE = 25
    MEMBER_MOVE = 26
    MEMBER_DISCONNECT = 27
    BOT_ADD = 28
    ROLE_CREATE = 30
    ROLE_UPDATE = 31
    ROLE_DELETE = 32
    INVITE_CREATE = 40
    INVITE_UPDATE = 41
    INVITE_DELETE = 42
    WEBHOOK_CREATE = 50
    WEBHOOK_UPDATE = 51
    WEBHOOK_DELETE = 52
    EMOJI_CREATE = 60
    EMOJI_UPDATE = 61
    EMOJI_DELETE = 62
    MESSAGE_DELETE = 72
    MESSAGE_BULK_DELETE = 73
    MESSAGE_PIN = 74
    MESSAGE_UNPIN = 75
    INTEGRATION_CREATE = 80
    INTEGRATION_UPDATE = 81
    INTEGRATION_DELETE = 82
    STAGE_INSTANCE_CREATE = 83
    STAGE_INSTANCE_UPDATE = 84
    STAGE_INSTANCE_DELETE = 85
    STICKER_CREATE = 90
    STICKER_UPDATE = 91
    STICKER_DELETE = 92
    THREAD_CREATE = 110
    THREAD_UPDATE = 111
    THREAD_DELETE = 112


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
    # noqa: E501
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
    # noqa: E501
    webhooks: List[Webhook]
    users: List[User]
    audit_log_entries: List[AuditLogEntry]
    integrations: List[Integration]
    threads: List[Channel]
