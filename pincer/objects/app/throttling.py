# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, DefaultDict

from .throttle_scope import ThrottleScope
from ..app.command import InteractableStructure
from ...exceptions import CommandCooldownError
from ...utils.slidingwindow import SlidingWindow

if TYPE_CHECKING:
    from typing import Dict, Optional

    from ...utils.types import Coro


class ThrottleInterface(ABC):
    """An ABC for throttling."""

    throttle: DefaultDict[
        Coro, Dict[Optional[str], SlidingWindow]
    ] = DefaultDict(dict)

    @staticmethod
    @abstractmethod
    def handle(command: InteractableStructure, **kwargs):
        raise NotImplementedError


class DefaultThrottleHandler(ThrottleInterface, ABC):
    """The default throttle-handler based off the
    :class:`~pincer.objects.app.throttling.ThrottleInterface` ABC
    """

    __throttle_scopes = {
        ThrottleScope.GLOBAL: None,
        ThrottleScope.GUILD: "guild_id",
        ThrottleScope.CHANNEL: "channel_id",
        ThrottleScope.USER: "author.user.id",
    }

    @staticmethod
    def get_key_from_scope(command: InteractableStructure) -> Optional[int]:
        """Retrieve the appropriate key from the context through the
        throttle scope.

        Parameters
        ----------
        ctx : :class:`~pincer.objects.message.context.MessageContext`
            The context to retrieve with

        Returns
        -------
        Optional[:class:`int`]
            The throttle-scope enum
        """
        scope = DefaultThrottleHandler.__throttle_scopes[command.cooldown_scope]

        if not scope:
            return None

        last_obj = command

        for attr in scope.split("."):
            last_obj = getattr(last_obj, attr)

        return last_obj

    @staticmethod
    def init_throttler(
        command: InteractableStructure, throttle_key: Optional[int]
    ):
        DefaultThrottleHandler.throttle[command.call][
            throttle_key
        ] = SlidingWindow(command.cooldown, command.cooldown_scale)

    @staticmethod
    def handle(command: InteractableStructure, **kwargs):
        if command.cooldown <= 0:
            return

        throttle_key = DefaultThrottleHandler.get_key_from_scope(command)
        group = DefaultThrottleHandler.throttle.get(command.call)
        window_slider = group.get(throttle_key) if group is not None else None

        if window_slider:
            if not window_slider.allow():
                raise CommandCooldownError(
                    f"Cooldown for command {command.app.name} not met!", command
                )
        else:
            DefaultThrottleHandler.init_throttler(command, throttle_key)
            DefaultThrottleHandler.handle(command)
