# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from inspect import getfullargspec, Parameter, Signature
from typing import Any, Union, Callable, Mapping, List

from .types import Coro, TypeCache
from ..objects.message.context import MessageContext


def should_pass_cls(call: Union[Coro, Callable[..., Any]]) -> bool:
    # TODO: fix docs
    """
    Checks whether a callable requires a self/cls as first parameter.

    Parameters
    ----------
    call: Union[Coro, Callable[..., Any]]
        The callable to check.

    Returns
    -------
    bool
        Whether the callable requires a self/cls as first parameter.
    """
    args = getfullargspec(call).args
    return len(args) >= 1 and args[0] in ["self", "cls"]


context_types = [Signature.empty, MessageContext]


def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool:
    # TODO: fix docs
    """

    Parameters
    ----------
    sig
    params

    Returns
    -------

    """
    if not params:
        return False

    annotation = sig[params[0]].annotation
    if isinstance(annotation, str):
        TypeCache()
        annotation = eval(annotation, TypeCache.cache, globals())

    return annotation in context_types
