from ...exceptions import CommandReturnIsEmpty as CommandReturnIsEmpty
from ...objects.app import CallbackType as CallbackType
from ..app.interactions import InteractionFlags as InteractionFlags
from ..message.file import File as File, create_form as create_form
from ..message.user_message import AllowedMentions as AllowedMentions
from .component import MessageComponent as MessageComponent
from .embed import Embed as Embed
from aiohttp import Payload as Payload
from typing import Dict, List, Optional, Tuple, Union

PILLOW_IMPORT: bool

class Message:
    content: str
    attachments: Optional[List[File]]
    tts: Optional[bool]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMentions]
    components: Optional[List[MessageComponent]]
    flags: Optional[InteractionFlags]
    delete_after: Optional[float]
    def __post_init__(self) -> None: ...
    @property
    def isempty(self) -> bool: ...
    def to_dict(self): ...
    def serialize(self, message_type: Optional[CallbackType] = ...) -> Tuple[str, Union[Payload, Dict]]: ...
