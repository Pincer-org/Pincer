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
from typing import Union, List, Optional

from .embed import Embed
from .interaction_base import CallbackType
from .interactions import InteractionFlags
from .message_component import MessageComponent
from .role import Role
from .user import User
from .user_message import AllowedMentionTypes
from ..exceptions import CommandReturnIsEmpty
from ..utils import APIObject, Snowflake


@dataclass
class AllowedMentions(APIObject):
    parse: List[AllowedMentionTypes]
    roles: List[Union[Role, Snowflake]]
    users: List[Union[User, Snowflake]]
    reply: bool = True

    def to_dict(self):
        def get_str_id(obj: Union[Snowflake, User, Role]) -> str:
            if hasattr(obj, "id"):
                obj = obj.id

            return str(obj)

        return {
            "parse": self.parse,
            "roles": list(map(get_str_id, self.roles)),
            "users": list(map(get_str_id, self.users)),
            "replied_user": self.reply
        }


@dataclass
class Message:
    content: str
    tts: Optional[bool] = False
    embeds: Optional[List[Embed]] = None
    allowed_mentions: Optional[AllowedMentions] = None
    components: Optional[List[MessageComponent]] = None
    flags: Optional[InteractionFlags] = None
    type: Optional[CallbackType] = None

    def to_dict(self):
        if len(self.content) < 1:
            raise CommandReturnIsEmpty("Cannot return empty message.")

        allowed_mentions = self.allowed_mentions.to_dict() \
            if self.allowed_mentions \
            else {}

        resp = {
            "content": self.content,
            "tts": self.tts,
            "flags": self.flags,
            "embeds": [embed.to_dict() for embed in (self.embeds or [])],
            "allowed_mentions": allowed_mentions,
            "components": [
                components.to_dict() for components in (self.components or [])
            ]
        }

        return {
            "type": self.type or CallbackType.MESSAGE,
            "data": {k: i for k, i in resp.items() if i}
        }
