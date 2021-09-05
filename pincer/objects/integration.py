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

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from pincer.objects.user import User
from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, OptionallyProvided
from pincer.utils.snowflake import Snowflake

class IntegrationExpireBehavior(Enum):
	"""Represents a Discord Integration expire behavior"""
	REMOVE_ROLE = 0
	KICK = 1

@dataclass
class IntegrationAccount(APIObject):
	"""Represents a Discord Integration Account object
	
	:param id: id of the account
	:param name: name of the account"""
	id: str
	name: str

@dataclass
class IntegrationApplication(APIObject):
	"""Represents a Discord Integration Application object
	
	:param id: the id of the app
	:param name: the name of the app
	:param icon: the icon hash of the app
	:param description: the description of the app
	:param summary: the summary of the app
	:param bot: the bot associated with this application
	"""
	id: Snowflake
	name: str
	icon: Optional[str]
	description: str
	summary: str
	bot: OptionallyProvided[User] = MISSING

@dataclass
class Integration(APIObject):
	"""Represents a Discord Integration object

	:param id: integration id
	:param name: integration name
	:param type: integration type (twitch, youtube, or discord)
	:param enabled: is this integration enabled
	:param syncing: is this integration syncing
	:param role_id: id that this integration uses for subscribers
	:param enable_emoticons: whether emoticons should be synced for this integration (twitch only currently)
	:param expire_behavior: the behavior of expiring subscribers
	:param expire_grace_period: the grace period (in days) before expiring subscribers
	:param user: user for this integration
	:param account: integration account information
	:param synced_at: when this integration was last synced
	:param subscriber_count: how many subscribers this integration has
	:param revoked: has this integration been revoked
	:param application: The bot/OAuth2 application for discord integrations
	"""

	id: Snowflake
	name: str
	type: str
	enabled: bool
	account: IntegrationAccount

	syncing: OptionallyProvided[bool] = MISSING
	role_id: OptionallyProvided[Snowflake] = MISSING
	enable_emoticons: OptionallyProvided[bool] = MISSING
	expire_behavior: OptionallyProvided[IntegrationExpireBehavior] = MISSING
	expire_grace_period: OptionallyProvided[int] = MISSING
	user: OptionallyProvided[User] = MISSING
	synced_at: OptionallyProvided[str] = MISSING
	subscriber_count: OptionallyProvided[int] = MISSING
	revoked: OptionallyProvided[bool] = MISSING
	application: OptionallyProvided[IntegrationApplication] = MISSING

	def set_synced_at(self, time: datetime):
		self.synced_at = time.isoformat()