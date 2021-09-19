"""
Pincer library
====================
An asynchronous python API wrapper meant to replace discord.py

:copyright: (c) 2021-present Pincer
:license: MIT, see LICENSE for more details.
"""

__title__ = "Pincer library"
__package__ = "pincer"
__author__ = "Sigmanificient, Arthurdw"
__license__ = "MIT"
__version__ = "0.6.9-dev"
__description__ = "Discord API wrapper rebuild from scratch."

from pincer.client import Client, Bot
from pincer.commands import command
from pincer.objects import Intents

__all__ = ("Client", "Bot", "command", "Intents")
