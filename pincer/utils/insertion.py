# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, Union, Callable, Mapping, List
from inspect import getfullargspec, Parameter, Signature

from .types import Coro
from ..objects.message.context import MessageContext


def should_pass_cls(call: Union[Coro, Callable[..., Any]]) -> bool:
    args = getfullargspec(call).args
    return len(args) >= 1 and args[0] in ["self", "cls"]


context_types = [Signature.empty, MessageContext]


def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool:
    # ? this is an internal function lmao
    return len(params) >= 1 and sig[params[0]].annotation in context_types
