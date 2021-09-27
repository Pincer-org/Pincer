"""
Pincer library
====================
An asynchronous python API wrapper meant to replace discord.py

Copyright Pincer 2021
Full MIT License can be found in `LICENSE` at the project root.
"""

from typing import NamedTuple, Literal

from pincer.client import Client, Bot
from pincer.commands import command
from pincer.objects import Intents

__package__ = "pincer"
__title__ = "Pincer library"
__description__ = "Discord API wrapper rebuild from scratch."
__author__ = "Sigmanificient, Arthurdw"
__email__ = "contact@pincer.org"
__license__ = "MIT"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: Literal["alpha", "beta", "candidate", "final", "dev"]
    serial: int

    def __repr__(self) -> str:
        return (
            f'{self.major}.{self.minor}.{self.micro}'
            f'-{self.release_level}{self.serial}'
        )


__version__ = VersionInfo(0, 7, 0, 'dev', 0)
__all__ = (
    "__version__", "__title__", "__package__",
    "__author__", "__email__",
    "Client", "Bot", "command", "Intents"
)
