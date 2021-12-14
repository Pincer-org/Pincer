from typing import Any, Callable, Iterable, List, T


def replace(
    func: Callable[[Any], bool], iter: Iterable[T], new_item: T
) -> List[T]:
    return [
        item if func(item) else new_item
        for item in iter
    ]
