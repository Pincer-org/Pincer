# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

import logging
from glob import glob
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from ..utils.directory import chdir

if TYPE_CHECKING:
    from typing import Dict
    from ..utils.types import Coro

from .channel_create import channel_create_middleware
from .error import error_middleware
from .guild_create import guild_create_middleware
from .interaction_create import (
    convert_message, interaction_response_handler, interaction_handler,
    interaction_create_middleware
)
from .message_create import message_create_middleware
from .message_delete import on_message_delete_middleware
from .message_update import message_update_middleware
from .payload import payload_middleware
from .ready import on_ready_middleware
from .voice_state_update import voice_state_update_middleware

_log = logging.getLogger(__package__)


def get_middleware() -> Dict[str, Coro]:
    middleware_list: Dict[str, Coro] = {}

    with chdir(Path(__file__).parent.resolve()):

        for middleware_path in glob("*.py"):
            if middleware_path.startswith("__"):
                continue

            event = middleware_path[:-3]

            try:
                middleware_list[event] = getattr(
                    import_module(f".{event}", package=__name__),
                    "export"
                )()
            except AttributeError:
                _log.warning(
                    f"Middleware {middleware_path} expected an `export` method."
                )

                continue

                # raise NoExportMethod(
                #    f"Middleware module `{middleware_path}` expected an "
                #    "`export` method but none was found!"
                # )

    return middleware_list


middleware: Dict[str, Coro] = get_middleware()


__all__ = (
    "channel_create_middleware", "error_middleware",
    "guild_create_middleware", "convert_message",
    "interaction_response_handler", "interaction_handler",
    "interaction_create_middleware", "message_create_middleware",
    "on_message_delete_middleware", "message_update_middleware",
    "payload_middleware", "on_ready_middleware",
    "voice_state_update_middleware"
)
