# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

import logging
from glob import glob
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Dict

from ..utils.directory import chdir

if TYPE_CHECKING:
    from ..utils.types import Coro

from .activity_join_request import *
from .activity_join import *
from .activity_spectate import *
from .channel_create import *
from .error import *
from .guild_create import *
from .guild_status import *
from .interaction_create import *
from .message_create import *
from .message_delete import *
from .message_update import *
from .notification_create import *
from .payload import *
from .ready import *
from .speaking_start import *
from .speaking_stop import *
from .voice_channel_select import *
from .voice_connection_status import *
from .voice_settings_update import *
from .voice_state_create import *
from .voice_state_delete import *
from .voice_state_update import *

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
