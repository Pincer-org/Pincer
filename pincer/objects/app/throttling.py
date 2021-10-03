# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .throttle_scope import ThrottleScope
from ...exceptions import CommandCooldownError
from ...utils.slidingwindow import SlidingWindow

if TYPE_CHECKING:
    from typing import Dict, Optional
    from ..message.context import MessageContext
    from ...utils import Coro


class ThrottleInterface(ABC):
    throttle: Dict[Coro, Dict[Optional[str], SlidingWindow]] = {}

    @staticmethod
    @abstractmethod
    def handle(ctx: MessageContext, **kwargs):
        """
        Handles a context. This method is executed before the command is.

        :param ctx:
            The context of the command.

        :param kwargs:
            The extra kwargs passed for the cooldown.
        """
        raise NotImplementedError


class DefaultThrottleHandler(ThrottleInterface, ABC):
    __throttle_scopes = {
        ThrottleScope.GLOBAL: None,
        ThrottleScope.GUILD: "guild_id",
        ThrottleScope.CHANNEL: "channel_id",
        ThrottleScope.USER: "author.user.id"
    }

    @staticmethod
    def get_key_from_scope(ctx: MessageContext) -> Optional[int]:
        """
        Retrieve the the appropriate key from the context through the
        throttle scope.
        """
        scope = DefaultThrottleHandler.__throttle_scopes[
            ctx.command.cooldown_scope]

        if not scope:
            return None

        last_obj = ctx

        for attr in scope.split("."):
            last_obj = getattr(last_obj, attr)

        return last_obj

    @staticmethod
    def init_throttler(ctx: MessageContext, throttle_key: Optional[int]):
        DefaultThrottleHandler.throttle[ctx.command.call][throttle_key] \
            = SlidingWindow(ctx.command.cooldown, ctx.command.cooldown_scale)

    @staticmethod
    def handle(ctx: MessageContext, **kwargs):
        if ctx.command.cooldown <= 0:
            return

        throttle_key = DefaultThrottleHandler.get_key_from_scope(ctx)
        group = DefaultThrottleHandler.throttle.get(ctx.command.call)
        window_slider = group.get(throttle_key) if group is not None else None

        if window_slider:
            if not window_slider.allow():
                raise CommandCooldownError(
                    f"Cooldown for command {ctx.command.app.name} not met!",
                    ctx
                )
        else:
            DefaultThrottleHandler.init_throttler(ctx, throttle_key)
            DefaultThrottleHandler.handle(ctx)
