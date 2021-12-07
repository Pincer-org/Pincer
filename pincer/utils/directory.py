# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from contextlib import contextmanager
from os import getcwd, chdir as os_chdir
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Generator, Any, Union


@contextmanager
def chdir(path: Union[str, Path]) -> Generator[str, Any, None]:
    """Change the cwd to the given path as a context manager.

    Parameters
    ----------
    path:
        Path to change to.

    Yields
    ------
    Generator[:class:`str`, Any, None]
    """
    current_path = getcwd()
    os_chdir(path)

    yield current_path
    os_chdir(current_path)
