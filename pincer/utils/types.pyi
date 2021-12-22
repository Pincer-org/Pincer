from typing import Any, Callable, Coroutine, Optional, TypeVar, Union

class MissingType:
    def __bool__(self) -> bool: ...
    def __eq__(self, __o: object) -> bool: ...
    def __hash__(self) -> int: ...

MISSING: Any
T = TypeVar('T')
JSONSerializable = TypeVar('JSONSerializable', str, int, float, list, dict, bool, None)
APINullable = Union[T, MissingType]
Coro = TypeVar('Coro', bound=Callable[..., Coroutine[Any, Any, Any]])
choice_value_types = Union[str, int, float]
CheckFunction = Optional[Callable[[Any], bool]]

class Singleton(type):
    def __call__(cls, *args, **kwargs): ...

class TypeCache(metaclass=Singleton):
    cache: Any
    def __init__(self) -> None: ...
