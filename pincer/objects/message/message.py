# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from json import dumps
from typing import TYPE_CHECKING

from aiohttp import FormData, Payload

from ..message.file import File
from ...exceptions import CommandReturnIsEmpty

PILLOW_IMPORT = True

try:
    from PIL.Image import Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False

if TYPE_CHECKING:
    from typing import Dict, Tuple, Union, List, Optional

    from ...objects.app import CallbackType
    from ..message.embed import Embed
    from ..message.user_message import AllowedMentions
    from ..app import InteractionFlags
    from .component import MessageComponent


@dataclass
class Message:
    # TODO: Docs for tts, allowed_mentions, components, flags, and type.

    """
    A discord message that will be send to discord

    :param content:
        The text in the message.

    :param attachments:
        Attachments on the message. This is a File object. You can also attach
        a Pillow Image or string. Pillow images will be converted to PNGs. They
        will use the naming sceme ``image%`` where % is the images index in the
        attachments array. Strings will be read as a filepath. The name of the
        file that the string points to will be used as the name.

    :param embeds:
        Embed attached to the message. This is an Embed object.
    """
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
        """
        :return:
            Returns true if a message is empty.
        """

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

    # TODO: Write docs.
    def serialize(
        self, message_type: Optional[CallbackType] = None
    ) -> Tuple[str, Union[Payload, Dict]]:
        """
        Creates the data that the discord API wants for the message object

        :return: (content_type, data)

        :raises CommandReturnIsEmpty:
            Command does not have content, an embed, or attachment.
        """

        if self.isempty:
            raise CommandReturnIsEmpty("Cannot return empty message.")

        json_payload = self.to_dict()

        if message_type is not None:
            json_data = json_payload
            json_payload = {
                "data": json_data,
                "type": message_type
            }

        if not self.attachments:
            return "application/json", json_payload

        form = FormData()
        form.add_field("payload_json", dumps(json_payload))

        for file in self.attachments:
            form.add_field("file", file.content, filename=file.filename)

        payload = form()
        return payload.headers["Content-Type"], payload
