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
                    import_module(f".{event}", package=__name__), "export"
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
