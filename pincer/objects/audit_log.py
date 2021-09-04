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

from pincer.objects.channel import Channel
from pincer.objects.user import User
from pincer.objects.webhook import Webhook
from pincer.utils.api_object import APIObject
from pincer.utils.constants import OptionallyProvided, MISSING
from pincer.utils.snowflake import Snowflake

class AuditLogEvent(Enum):
	# TODO: Write documentation
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
	# TODO: Write documentation
	new_value: Any
	old_value: Any
	key: str

@dataclass
class AuditEntryInfo(APIObject):
	# TODO: Write documentation
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
	# TODO: Write documentation
	target_id: Optional[str]
	user_id: Optional[Snowflake]
	id: Snowflake
	action_type: int
	
	changes: OptionallyProvided[List[AuditLogChange]] = MISSING
	options: OptionallyProvided[AuditEntryInfo] = MISSING
	reason: OptionallyProvided[str] = MISSING

@dataclass
class AuditLog(APIObject):
	# TODO: Write documentation
	webhooks: List[Webhook]
	users: List[User]
	audit_log_entries: List[AuditLogEntry]
	integrations: List[...]
	threads: List[Channel]