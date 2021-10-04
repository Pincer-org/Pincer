# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations
from dataclasses import dataclass
from io import BytesIO
import os
from typing import Optional

from PIL.Image import Image

from ..utils import APIObject

@dataclass
class File(APIObject):
    """
    A file that is prepared by the user to be send to the discord
    API.

    :param content:
        file bytes

    :param filename:
        the name of the file when its uploaded to discord
    """

    content: bytes
    filename: str

    @classmethod
    def from_file(cls, filepath: str, filename: str=None) -> File:

        file = open(filepath,"rb").read()

        return cls(
            content=file,
            filename=filename or os.path.basename(filepath)
        )

    @classmethod
    def from_image(cls, img: Image, filename: str, format: Optional[str]=None) -> File:
        """
        Creates a file object from a PIL image
        Supports PNG and JPEG
        
        :return: File
        """

        if format is None:
            format = os.path.splitext(filename)[1][1:]

            if format == "jpg": format = "jpeg"

        imgByteArr = BytesIO()
        img.save(imgByteArr, format=format)
        img_bytes = imgByteArr.getvalue()

        return cls(
            content=img_bytes,
            filename=filename
        )