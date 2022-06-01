# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import os
from base64 import b64encode
from dataclasses import dataclass
from io import BytesIO
from json import dumps
from typing import TYPE_CHECKING

from aiohttp import FormData, Payload

from ...exceptions import ImageEncodingError

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple

    IMAGE_TYPE = Any

PILLOW_IMPORT = True


try:
    from PIL.Image import Image

    if TYPE_CHECKING:
        IMAGE_TYPE = Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False


def create_form(
    json_payload: Dict[Any], files: List[File]
) -> Tuple[str, Payload]:
    """
    Creates an aiohttp payload from an array of File objects.

    json_payload : Dict[Any]
        The json part of the request
    files : List[`~pincer.objects.message.file.File`]
        A list of files to be used in the request.

    Returns
    -------
    Tuple[str, :class:`aiohttp.Payload`]
        The content type and the payload to be sent in an HTTP request.
    """
    form = FormData()
    form.add_field("payload_json", dumps(json_payload))

    for file in files:
        if not file.filename:
            raise ImageEncodingError(
                "A filename is required for uploading attachments"
            )

        form.add_field("file", file.content, filename=file.filename)

    payload = form()
    return payload.headers["Content-Type"], payload


def _get_file_extension(filename: str) -> Optional[str]:
    """
    Returns the file extension from a str if it exists, otherwise
    return :data:`None`.

    filename : str
        The filename

    Returns
    -------
    Optional[:class:`str`]
        The file extension or :data:`None`
    """
    path = os.path.splitext(filename)
    if len(path) >= 2:
        return path[1][1:]
    return None


@dataclass
class File:
    """A file that is prepared by the user to be sent to the discord
    API.

    Attributes
    ----------
    content: :class:`bytes`
        File bytes.
    filename: :class:`str`
        The name of the file when it's uploaded to discord.
    """

    content: bytes
    image_format: str
    filename: Optional[str] = None

    @classmethod
    def from_file(cls, filepath: str, filename: str = None) -> File:
        """Make a ``File`` object from a file stored locally.

        Parameters
        ----------
        filepath: :class:`str`
            The path to the file you want to send. Must be string. The file's
            name in the file path is used as the name when uploaded to discord
            by default.

        filename: :class:`str`
            The name of the file. Will override the default name.
            |default| ``os.path.basename(filepath)``

        Returns
        -------
        :class:`~pincer.objects.message.file.File`
            The new file object.
        """
        with open(filepath, "rb") as data:
            file = data.read()

        return cls(
            content=file,
            image_format=_get_file_extension(filename),
            filename=filename or os.path.basename(filepath),
        )

    @classmethod
    def from_pillow_image(
        cls,
        img: IMAGE_TYPE,
        filename: Optional[str] = None,
        image_format: Optional[str] = None,
        **kwargs,
    ) -> File:
        """Creates a file object from a PIL image
        Supports GIF, PNG, JPEG, and WEBP.

        Parameters
        ----------
        img: :class:`~pil:PIL.Image.Image`
            Pillow image object.
        filename:
            The filename to be used when uploaded to discord. The extension is
            used as image_format unless otherwise specified.
        image_format:
            The image_format to be used if you want to override the file
            extension.

        Returns
        -------
        :class:`~pincer.objects.message.file.File`
            The new file object.

        Raises
        ------
        ModuleNotFoundError:
            ``Pillow`` is not installed
        """
        if not PILLOW_IMPORT:
            raise ModuleNotFoundError(
                "The `Pillow` library is required for sending and converting "
                "pillow images,"
            )

        if image_format is None:
            image_format = _get_file_extension(filename)

        if image_format == "jpg":
            image_format = "jpeg"

        # https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
        # Credit goes to second answer
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=image_format)
        img_bytes = img_byte_arr.getvalue()

        return cls(
            content=img_bytes, image_format=image_format, filename=filename
        )

    @property
    def uri(self) -> str:
        """
        Returns
        -------
        str
            The uri for the image.
            See `<https://discord.com/developers/docs/reference#api-versioning>`_.
        """  # noqa: E501
        if self.image_format not in {"jpeg", "png", "gif"}:
            raise ImageEncodingError(
                'Only image types "jpeg", "png", and "gif" can be sent in'
                " an Image URI"
            )

        encoded_bytes = b64encode(self.content).decode("ascii")

        return f"data:image/{self.image_format};base64,{encoded_bytes}"

    @property
    def content_type(self):
        return f"image/{self.image_format}"
