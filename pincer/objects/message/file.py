# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import os
from typing import Optional

from PIL.Image import Image

from ...utils import APIObject


@dataclass
class File(APIObject):
    """
    A file that is prepared by the user to be send to the discord
    API.

    :param content:
        File bytes.

    :param filename:
        The name of the file when its uploaded to discord.
    """

    content: bytes
    filename: str

    @classmethod
    def from_file(cls, filepath: str, filename: str = None) -> File:
        """
        :param filepath:
            The path to the file you want to send. Must be string. The file's
            name in the file path is used as the name when uploaded discord by
            default.

        :param filename:
            The name of the file. Will override the default name.
        """

        file = open(filepath, "rb").read()

        return cls(
            content=file,
            filename=filename or os.path.basename(filepath)
        )

    @classmethod
    def from_image(
        cls,
        img: Image,
        filename: str,
        image_format: Optional[str] = None
    ) -> File:
        """
        Creates a file object from a PIL image
        Supports PNG and JPEG

        :param img:
            Pillow image object.

        :param filename:
            The filename to be used when uploaded to discord. The extension is
            used as image_format unless otherwise specified.

        Keyword Arguments:

        :param image_format:
            The image_format to be used if you want to override the file
            extension.

        :return: File
        """

        if image_format is None:
            image_format = os.path.splitext(filename)[1][1:]

            if image_format == "jpg":
                image_format = "jpeg"

        imgByteArr = BytesIO()
        img.save(imgByteArr, format=image_format)
        img_bytes = imgByteArr.getvalue()

        return cls(
            content=img_bytes,
            filename=filename
        )
