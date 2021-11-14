# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import os
from dataclasses import dataclass
from io import BytesIO
from typing import Any
from typing import TYPE_CHECKING

from ...utils import APIObject

if TYPE_CHECKING:
    from typing import Optional


PILLOW_IMPORT = True

IMAGE_TYPE = Any

try:
    from PIL.Image import Image

    if TYPE_CHECKING:
        IMAGE_TYPE = Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False


@dataclass
class File(APIObject):
    """A file that is prepared by the user to be send to the discord
    API.

    Attributes
    ----------
    content: :class:`bytes`
        File bytes.
    filename: :class:`str`
        The name of the file when its uploaded to discord.
    """

    content: bytes
    filename: str

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
        """
        with open(filepath, "rb") as data:
            file = data.read()

        return cls(
            content=file,
            filename=filename or os.path.basename(filepath)
        )

    @classmethod
    def from_pillow_image(
            cls,
            img: IMAGE_TYPE,
            filename: str,
            image_format: Optional[str] = None,
            **kwargs
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
            image_format = os.path.splitext(filename)[1][1:]

            if image_format == "jpg":
                image_format = "jpeg"

        # https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
        # Credit goes to second answer
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=image_format)
        img_bytes = img_byte_arr.getvalue()

        return cls(
            content=img_bytes,
            filename=filename
        )
