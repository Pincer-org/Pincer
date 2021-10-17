from __future__ import annotations

import os
from typing import TYPE_CHECKING
from contextlib import contextmanager

if TYPE_CHECKING:
    from typing import Generator, Any


@contextmanager
def chdir(path: str) -> Generator[str, Any, None]:
    """Change the cwd to the given path as a context manager.

    Parameters
    ----------
    path:
        Path to change to.

    Yields
    ------
    Generator[:class:`str`, Any, None]
    """
    current_path = os.getcwd()
    os.chdir(path)

    yield current_path
    os.chdir(current_path)
