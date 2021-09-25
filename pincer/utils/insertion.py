# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from inspect import getfullargspec, Parameter, Signature
from typing import Any, Union, Callable, Mapping, List

from ..objects.context import Context
from .types import Coro


def should_pass_cls(call: Union[Coro, Callable[..., Any]]) -> bool:
    """
    Checks whether a callable requires a self/cls as first parameter.

    :param call:
        The callable to check.

    :return:
        Whether or not its required.
    """
    args = getfullargspec(call).args
    return len(args) >= 1 and args[0] in ["self", "cls"]


context_types = [Signature.empty, Context]


def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool:
    # TODO: Write docs
    return len(params) >= 1 and sig[params[0]].annotation in context_types
