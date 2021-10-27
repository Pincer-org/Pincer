# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from json import dumps
from typing import TYPE_CHECKING
from dataclasses import dataclass

from aiohttp import FormData, Payload

from ...exceptions import CommandReturnIsEmpty
from ..app.interaction_base import CallbackType

if TYPE_CHECKING:
    from typing import Dict, Union, List, Optional, Tuple


    from .embed import Embed
    from ..user.user import User
    from ..guild.role import Role
    from .component import MessageComponent
    from ...utils.snowflake import Snowflake
    from .user_message import AllowedMentionTypes
    from ..app.interactions import InteractionFlags

PILLOW_IMPORT = True

try:
    from PIL.Image import Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False

if TYPE_CHECKING:
    from ..message.embed import Embed
    from ..message.file import File
    from ..message.user_message import AllowedMentions
    from ..app import InteractionFlags
    from .component import MessageComponent


@dataclass
class AllowedMentions(APIObject):
    """Represents the entities the client can mention

    Attributes
    ----------
    parse: List[:class:`~pincer.objects.message.user_message.AllowedMentionTypes`]
        An array of allowed mention types to parse from the content.
    roles: List[Union[:class:`~pincer.objects.guild.role.Role`, :class:`~pincer.utils.snowflake.Snowflake`]]
        List of ``Role`` objects or snowflakes of allowed mentions.
    users: List[Union[:class:`~pincer.objects.user.user.User` :class:`~pincer.utils.snowflake.Snowflake`]]
        List of ``user`` objects or snowflakes of allowed mentions.
    reply: :class:`bool`
        If replies should mention the author.
        |default| :data:`True`
    """  # noqa: E501

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
    """A discord message that will be send to discord

    Attributes
    ----------
    content: :class:`str`
        The text in the message.
        |default| ``""``
    attachments: Optional[List[:class:`~pincer.objects.message.file.File`]]
        Attachments on the message. This is a File object. You can also attach
        a Pillow Image or string. Pillow images will be converted to PNGs. They
        will use the naming sceme ``image%`` where % is the images index in the
        attachments array. Strings will be read as a filepath. The name of the
        file that the string points to will be used as the name.
    tts: Optional[:class:`bool`]
        Whether the message should be spoken to the user.
        |default| :data:`False`
    embeds: Optional[List[:class:`~pincer.objects.message.embed.Embed`]]
        Embed attached to the message. This is an Embed object.
    allowed_mentions: Optional[:class:`~pincer.objects.message.message.AllowedMentions`]
        The allowed mentions for the message.
    components: Optional[List[:class:`~pincer.objects.message.component.MessageComponent`]]
        The components of the message.
    flags: Optional[:class:`~pincer.objects.app.interactions.InteractionFlags`]
        The interaction flags for the message.
    type: Optional[:class:`~pincer.objects.app.interaction_base.CallbackType`]
        The type of the callback.
    """  # noqa: E501

    content: str = ''
    attachments: Optional[List[File]] = None
    tts: Optional[bool] = False
    embeds: Optional[List[Embed]] = None
    allowed_mentions: Optional[AllowedMentions] = None
    components: Optional[List[MessageComponent]] = None
    flags: Optional[InteractionFlags] = None
    delete_after: Optional[float] = None

    def __post_init__(self):
        if self.delete_after and self.delete_after < 0:
            raise ValueError(
                "Message can not be deleted after a negative amount of "
                "seconds!"
            )

        if not self.attachments:
            return

        attch = []

        for count, value in enumerate(self.attachments):
            if isinstance(value, File):
                attch.append(value)
            elif PILLOW_IMPORT and isinstance(value, Image):
                attch.append(File.from_pillow_image(
                    value,
                    f"image{count}.png",
                ))
            elif isinstance(value, str):
                attch.append(File.from_file(value))
            else:
                raise ValueError(f"Attachment {count} is invalid type.")

        self.attachments = attch

    @property
    def isempty(self) -> bool:
        """:class:`bool`: If the message is empty."""

        return (
            len(self.content) < 1
            and not self.embeds
            and not self.attachments
        )

    def to_dict(self):

        allowed_mentions = (
            self.allowed_mentions.to_dict()
            if self.allowed_mentions else {}
        )

        # Attachments aren't serialized
        # because they are not sent as part of the json
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

        # IDE does not recognise return type of filter properly.
        # noinspection PyTypeChecker
        return dict(filter(
            lambda kv: kv[1],
            resp.items()
        ))

    def serialize(self) -> Tuple[str, Union[Payload, Dict]]:
        """
        Creates the data that the discord API wants for the message object

        :return: (content_type, data)

        :raises CommandReturnIsEmpty:
            Command does not have content, an embed, or attachment.
        """
        if self.isempty:
            raise CommandReturnIsEmpty("Cannot return empty message.")

        if not self.attachments:
            return "application/json", self.to_dict()

        form = FormData()
        form.add_field("payload_json", dumps(self.to_dict()))

        for file in self.attachments:
            form.add_field("file", file.content, filename=file.filename)

        payload = form()
        return payload.headers["Content-Type"], payload
