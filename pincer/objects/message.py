# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Dict, Tuple, Union, List, Optional, TYPE_CHECKING

import aiohttp

from .embed import Embed
from .interaction_base import CallbackType
from .file import File
from .role import Role
from .user import User
from .user_message import AllowedMentionTypes
from ..exceptions import CommandReturnIsEmpty
from ..utils import APIObject, Snowflake

if TYPE_CHECKING:
    from .interactions import InteractionFlags
    from .message_component import MessageComponent


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
    attachments: Optional[File] = None
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

    def serialize(self) -> Tuple[str,Union[bytes,Dict]]:
        """
        Creates the information that the discord API wants for the message
        object
        """

        if self.attachments:
            form = aiohttp.FormData()
            form.add_field("payload_json",json.dumps(self.to_dict()))
            
            for file in self.attachments:
                form.add_field("file",file.content,filename=file.filename)


            payload = form()
            return payload.headers["Content-Type"], payload

        else:
            return "application/json", self.to_dict()
