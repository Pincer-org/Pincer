# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Any, Optional

from .context import Context
from ..utils.slidingwindow import SlidingWindow


class ThrottleScope(Enum):
    """
    On what the cooldown should be set/on what should the cooldown be
    set.

    :param GUILD:
        The cooldown is per guild.

    :param CHANNEL:
        The cooldown is per channel.

    :param USER:
        The cooldown is per user.

    :param GLOBAL:
        The cooldown is global.
    """
    GUILD = auto()
    CHANNEL = auto()
    USER = auto()
    GLOBAL = auto()


class ThrottleInterface(ABC):
    @abstractmethod
    def __init__(self, client, **kwargs):
        """
        Initializes a throttler.

        :param client:
            The current connected client, aka your bot.

        :param kwargs:
            Optional extra arguments.
        """
        self.client = client

    @abstractmethod
    async def handle(self, ctx: Context, **kwargs):
        """
        Handles a context. This method is executed before the command is.

        :param ctx:
            The context of the command.

        :param kwargs:
            The extra kwargs passed for the cooldown.
        """
        raise NotImplementedError


class DefaultThrottleHandler(ThrottleInterface, ABC):
    default_throttle_type = ThrottleScope.GLOBAL
    throttle: Dict[Any, SlidingWindow] = {}

    __throttle_scopes = {
        ThrottleScope.GLOBAL: None,
        ThrottleScope.GUILD: "guild.id",
        ThrottleScope.CHANNEL: "channel.id",
        ThrottleScope.USER: "author.id"
    }

    def get_key_from_scope(
            self,
            ctx: Context,
            scope: ThrottleScope
    ) -> Optional[int]:
        """
        Retrieve the the appropriate key from the context through the
        throttle scope.
        """
        ...

    async def handle(self, ctx: Context, **kwargs):
        ...
