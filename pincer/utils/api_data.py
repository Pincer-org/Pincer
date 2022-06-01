# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import Generic, TypeVar, TYPE_CHECKING

from pincer.utils import APIObject

if TYPE_CHECKING:
    from typing import Any, Coroutine, List, Type, Generator, AsyncIterator

T = TypeVar("T")


class APIDataGen(Generic[T]):
    def __init__(
        self, factory: Type[T], request_func: Coroutine[Any, None, Any]
    ):

        self.fac = (
            factory if isinstance(factory, APIObject) else factory.from_dict
        )
        self.request_func = request_func

    async def __async(self) -> List[T]:
        data = await self.request_func
        return [self.fac(i) for i in data]

    def __await__(self) -> Generator[Any, None, Any]:
        return self.__async().__await__()

    async def __aiter__(self) -> AsyncIterator[List[T]]:
        for item in await self:
            yield self.fac(item)
