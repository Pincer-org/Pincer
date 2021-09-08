# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, List

from ..objects.channel import Channel
from ..objects.integration import Integration
from ..objects.user import User
from ..objects.webhook import Webhook
from ..utils import APIObject, APINullable, MISSING, Snowflake


class AuditLogEvent(Enum):
    """
    Audit log action type.
    This represents the action which got performed,
    and logged.
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
    """
    Representation of Discord Audit Log Change object

    :param new_value:
        new value of the key

    :param old_value:
        old value of the key

    :param key:
        name of audit log change key
    """
    new_value: Any
    old_value: Any
    key: str


@dataclass
class AuditEntryInfo(APIObject):
    """
    Represents Discord Optional Audit Entry Info

    :param delete_member_days:
        number of days after which inactive members were kicked

    :param members_removed:
        number of members removed by the prune

    :param channel_id:
        channel in which the entities were targeted

    :param message_id:
        id of the message that was targeted

    :param count:
        number of entities that were targeted

    :param id:
        id of the overwritten entity

    :param type:
        type of overwritten entity - "0" for "role" or "1" for "member"

    :param role_name:
        name of the role if type is "0" (not present if type is "1")
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
    """
    Represents a Discord Audit Log Entry object.

    :param target_id:
        id of the affected entity x(webhook, user, role, etc.)

    :param changes:
        changes made to the target_id

    :param user_id:
        the user who made the changes

    :param id:
        id of the entry

    :param action_type:
        type of action that occurred

    :param options:
        additional info for certain action types

    :param reason:
        the reason for the change x(0-512 characters)
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
    """
    Represents a Discord Audit Log object.

    :param webhooks:
        list of webhooks found in the audit log

    :param users:
        list of users found in the audit log

    :param audit_log_entries:
        list of audit log entries

    :param integrations:
        list of partial integration objects

    :param threads:
        list of threads found in the audit log
    """
    webhooks: List[Webhook]
    users: List[User]
    audit_log_entries: List[AuditLogEntry]
    integrations: List[Integration]
    threads: List[Channel]
