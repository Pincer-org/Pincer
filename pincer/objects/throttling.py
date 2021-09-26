# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from abc import ABC, abstractmethod
from typing import Dict, Optional

from .message_context import MessageContext
from .throttle_scope import ThrottleScope
from ..exceptions import CommandCooldownError
from ..utils import Coro
from ..utils.slidingwindow import SlidingWindow


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
    async def handle(self, ctx: MessageContext, **kwargs):
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
    throttle: Dict[Coro, Dict[Optional[str], SlidingWindow]] = {}

    __throttle_scopes = {
        ThrottleScope.GLOBAL: None,
        ThrottleScope.GUILD: "guild_id",
        ThrottleScope.CHANNEL: "channel_id",
        ThrottleScope.USER: "author.id"
    }

    def get_key_from_scope(
            self,
            ctx: MessageContext,
            scope: ThrottleScope
    ) -> Optional[int]:
        """
        Retrieve the the appropriate key from the context through the
        throttle scope.
        """
        scope = self.__throttle_scopes[scope]

        if not scope:
            return None

        last_obj = ctx

        for attr in scope.split("."):
            last_obj = getattr(last_obj, attr)

        return last_obj

    def handle(self, ctx: MessageContext, **kwargs):
        throttle_key = self.get_key_from_scope(ctx, ctx.command.cooldown_scope)
        window_slider = self.throttle.get(ctx.command.call).get(throttle_key)

        if window_slider and not window_slider.allow():
            raise CommandCooldownError(
                f"Cooldown for command {ctx.command.app.name} not met!",
                ctx
            )
