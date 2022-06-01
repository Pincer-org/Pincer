# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, Callable, Iterable, List, T


def replace(
    func: Callable[[Any], bool], iter_: Iterable[T], new_item: T
) -> List[T]:
    return [item if func(item) else new_item for item in iter_]
