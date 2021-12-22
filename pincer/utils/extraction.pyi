from typing import Any, Optional, TypeVar

T = TypeVar('T')

class GetItem:
    def __getitem__(self, key: int) -> Any: ...

def get_index(collection: GetItem, index: int, fallback: Optional[T] = ...) -> Optional[T]: ...
