# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import TYPE_CHECKING, Tuple, List
from typing import Union

from ..objects.app.interaction_flags import InteractionFlags
from ..objects.message.component import MessageComponent
from ..objects.message.embed import Embed
from ..objects.message.file import File
from ..objects.message.message import Message

PILLOW_IMPORT = True

try:
    from PIL.Image import Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False

if TYPE_CHECKING:
    from pincer import Client

MessageConvertable = Union[Embed, Message, str, Tuple, List]


def convert_message(client: Client, message: MessageConvertable) -> Message:
    """
    Converts a message to a Message object.

    Parameters
    ----------
    client : :class:`~pincer.client.Client`
        The Client object for the bot
    message : MessageConvertable
        A value to be converted to a message

    Returns
    -------
    :class:`~pincer.objects.message.message.Message`
        The message object to be sent
    """
    if (
        message
        and isinstance(message, Iterable)
        and not isinstance(message, str)
    ):
        kwargs = defaultdict(list)
        for item in message:
            list_to_message_dict(item, kwargs)
        message = Message(**kwargs)
    elif isinstance(message, Embed):
        message = Message(embeds=[message])
    elif PILLOW_IMPORT and isinstance(message, (File, Image)):
        message = Message(attachments=[message])
    elif not isinstance(message, Message):
        message = (
            Message(message)
            if message
            else Message(
                client.received_message, flags=InteractionFlags.EPHEMERAL
            )
        )
    return message


def list_to_message_dict(item, kwargs):
    if isinstance(item, Embed):
        kwargs["embeds"].append(item)
    elif isinstance(item, File) or (PILLOW_IMPORT and isinstance(item, Image)):
        kwargs["attachments"].append(item)
    elif isinstance(item, MessageComponent):
        kwargs["components"].append(item)
    elif isinstance(item, str):
        kwargs["content"] = item
    elif isinstance(item, InteractionFlags):
        kwargs["flags"] = item
