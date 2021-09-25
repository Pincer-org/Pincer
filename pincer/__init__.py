"""
Pincer library
====================
An asynchronous python API wrapper meant to replace discord.py

Copyright Pincer 2021
Full MIT License can be found in `LICENSE` at the project root.
"""

__title__ = "Pincer library"
__package__ = "pincer"
__author__ = "Sigmanificient, Arthurdw"
__license__ = "MIT"
__version__ = "0.6.11-dev"
__description__ = "Discord API wrapper rebuild from scratch."

from pincer.client import Client, Bot
from pincer.commands import command
from pincer.objects import Intents

__all__ = ("Client", "Bot", "command", "Intents")
