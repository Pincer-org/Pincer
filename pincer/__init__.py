"""
Pincer library
====================
An asynchronous python API wrapper meant to replace discord.py

Copyright Pincer 2021
Full MIT License can be found in `LICENSE` at the project root.
"""

from typing import NamedTuple, Literal, Optional

from ._config import GatewayConfig
from .client import event_middleware, Client, Bot
from .cog import Cog
from .commands import command, ChatCommandHandler
from .exceptions import (
    PincerError,
    InvalidPayload,
    UnhandledException,
    NoExportMethod,
    CogError,
    CogNotFound,
    CogAlreadyExists,
    NoValidSetupMethod,
    TooManySetupArguments,
    NoCogManagerReturnFound,
    CommandError,
    CommandCooldownError,
    CommandIsNotCoroutine,
    CommandAlreadyRegistered,
    CommandDescriptionTooLong,
    TooManyArguments,
    InvalidArgumentAnnotation,
    CommandReturnIsEmpty,
    InvalidCommandGuild,
    InvalidCommandName,
    InvalidEventName,
    InvalidUrlError,
    EmbedFieldError,
    TaskError,
    TaskAlreadyRunning,
    TaskCancelError,
    TaskIsNotCoroutine,
    TaskInvalidDelay,
    DispatchError,
    DisallowedIntentsError,
    InvalidTokenError,
    HeartbeatError,
    UnavailableGuildError,
    HTTPError,
    NotModifiedError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    MethodNotAllowedError,
    RateLimitError,
    GatewayError,
    ServerError,
    EmbedOverflow,
    ImageEncodingError,
)
from .objects import Intents

__package__ = "pincer"
__title__ = "Pincer library"
__description__ = "Discord API wrapper rebuild from scratch."
__author__ = "Sigmanificient, Arthurdw"
__email__ = "contact@pincer.dev"
__license__ = "MIT"

ReleaseType = Optional[Literal["alpha", "beta", "candidate", "final", "dev"]]


class VersionInfo(NamedTuple):
    """A Class representing the version of the Pincer library."""

    major: int
    minor: int
    micro: int

    release_level: ReleaseType = None
    serial: int = 0

    def __repr__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}" + (
            f"-{self.release_level}{self.serial}"
            * (self.release_level is not None)
        )


version_info = VersionInfo(0, 16, 1)
__version__ = repr(version_info)

__all__ = (
    "BadRequestError",
    "Bot",
    "ChatCommandHandler",
    "Client",
    "Cog",
    "CogAlreadyExists",
    "CogError",
    "CogNotFound",
    "CommandAlreadyRegistered",
    "CommandCooldownError",
    "CommandDescriptionTooLong",
    "CommandError",
    "CommandIsNotCoroutine",
    "CommandReturnIsEmpty",
    "DisallowedIntentsError",
    "DispatchError",
    "EmbedFieldError",
    "EmbedOverflow",
    "ForbiddenError",
    "GatewayConfig",
    "GatewayError",
    "HTTPError",
    "HeartbeatError",
    "ImageEncodingError",
    "Intents",
    "InvalidArgumentAnnotation",
    "InvalidCommandGuild",
    "InvalidCommandName",
    "InvalidEventName",
    "InvalidPayload",
    "InvalidTokenError",
    "InvalidUrlError",
    "MethodNotAllowedError",
    "NoCogManagerReturnFound",
    "NoExportMethod",
    "NoValidSetupMethod",
    "NotFoundError",
    "NotModifiedError",
    "PincerError",
    "RateLimitError",
    "ServerError",
    "TaskAlreadyRunning",
    "TaskCancelError",
    "TaskError",
    "TaskInvalidDelay",
    "TaskIsNotCoroutine",
    "TooManyArguments",
    "TooManySetupArguments",
    "UnauthorizedError",
    "UnavailableGuildError",
    "UnhandledException",
    "__author__",
    "__email__",
    "__package__",
    "__title__",
    "__version__",
    "command",
    "event_middleware",
)
