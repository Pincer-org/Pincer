# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Union, List, Optional, TYPE_CHECKING

from ..app.interaction_base import CallbackType
from ..guild.role import Role
from ..message.embed import Embed
from ..message.user_message import AllowedMentionTypes
from ..user import User
from ...exceptions import CommandReturnIsEmpty
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake

if TYPE_CHECKING:
    from ..app import InteractionFlags
    from .component import MessageComponent


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
    # TODO: Write docs
    content: str = ''
    tts: Optional[bool] = False
    embeds: Optional[List[Embed]] = None
    allowed_mentions: Optional[AllowedMentions] = None
    components: Optional[List[MessageComponent]] = None
    flags: Optional[InteractionFlags] = None
    type: Optional[CallbackType] = None

    def to_dict(self):
        if len(self.content) < 1 and not self.embeds:
            raise CommandReturnIsEmpty("Cannot return empty message.")

        allowed_mentions = (
            self.allowed_mentions.to_dict()
            if self.allowed_mentions else {}
        )

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
