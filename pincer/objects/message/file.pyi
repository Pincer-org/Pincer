from ...exceptions import ImageEncodingError as ImageEncodingError
from PIL.Image import Image
from aiohttp import Payload as Payload
from typing import Any, Dict, List, Optional, Tuple

IMAGE_TYPE = Any
PILLOW_IMPORT: bool
IMAGE_TYPE = Image

def create_form(json_payload: Dict[Any], files: List[File]) -> Tuple[str, Payload]: ...

class File:
    content: bytes
    image_format: str
    filename: Optional[str]
    @classmethod
    def from_file(cls, filepath: str, filename: str = ...) -> File: ...
    @classmethod
    def from_pillow_image(cls, img: IMAGE_TYPE, filename: Optional[str] = ..., image_format: Optional[str] = ..., **kwargs) -> File: ...
    @property
    def uri(self) -> str: ...
    @property
    def content_type(self): ...
