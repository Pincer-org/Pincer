from ..objects.app.interaction_flags import InteractionFlags as InteractionFlags
from ..objects.message.embed import Embed as Embed
from ..objects.message.file import File as File
from ..objects.message.message import Message as Message
from pincer import Client as Client
from typing import Union

PILLOW_IMPORT: bool
MessageConvertable = Union[Embed, Message, str]

def convert_message(client: Client, message: MessageConvertable) -> Message: ...
