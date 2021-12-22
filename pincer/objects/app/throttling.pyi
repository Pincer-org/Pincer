import abc
from ...exceptions import CommandCooldownError as CommandCooldownError
from ...utils.slidingwindow import SlidingWindow as SlidingWindow
from ...utils.types import Coro as Coro
from ..message.context import MessageContext as MessageContext
from .throttle_scope import ThrottleScope as ThrottleScope
from abc import ABC, abstractmethod
from typing import Dict, Optional

class ThrottleInterface(ABC, metaclass=abc.ABCMeta):
    throttle: Dict[Coro, Dict[Optional[str], SlidingWindow]]
    @staticmethod
    @abstractmethod
    def handle(ctx: MessageContext, **kwargs): ...

class DefaultThrottleHandler(ThrottleInterface, ABC):
    @staticmethod
    def get_key_from_scope(ctx: MessageContext) -> Optional[int]: ...
    @staticmethod
    def init_throttler(ctx: MessageContext, throttle_key: Optional[int]): ...
    @staticmethod
    def handle(ctx: MessageContext, **kwargs): ...
