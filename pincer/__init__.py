"""
Pincer library
====================
An asynchronous python API wrapper meant to replace discord.py

Copyright Pincer 2021
Full MIT License can be found in `LICENSE` at the project root.
"""

from typing import NamedTuple, Literal, Optional

from pincer.client import Client, Bot
from pincer.commands import command
from pincer.objects import Intents

__package__ = "pincer"
__title__ = "Pincer library"
__description__ = "Discord API wrapper rebuild from scratch."
__author__ = "Sigmanificient, Arthurdw"
__email__ = "contact@pincer.org"
__license__ = "MIT"

from pincer.utils import Choices

ReleaseType = Optional[Literal["alpha", "beta", "candidate", "final", "dev"]]


class VersionInfo(NamedTuple):
    """A Class representing the version of the Pincer library."""
    major: int
    minor: int
    micro: int

    release_level: ReleaseType = None
    serial: int = 0

    def __repr__(self) -> str:
        return (
            f'{self.major}.{self.minor}.{self.micro}'
            + (
                f'-{self.release_level}{self.serial}'
                * (self.release_level is not None)
            )
        )


__version__ = VersionInfo(0, 8, 0)
__all__ = (
    "Bot", "Choices", "Client", "Intents", "__author__", "__email__",
    "__package__", "__title__", "__version__", "command"
)
