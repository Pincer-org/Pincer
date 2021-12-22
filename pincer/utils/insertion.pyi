from ..objects.message.context import MessageContext as MessageContext
from .types import Coro as Coro, TypeCache as TypeCache
from inspect import Parameter
from typing import Any, Callable, List, Mapping, Union

def should_pass_cls(call: Union[Coro, Callable[..., Any]]) -> bool: ...

context_types: Any

def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool: ...
