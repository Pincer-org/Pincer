# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from inspect import getfullargspec, Parameter, Signature
from typing import Any, Union, Callable, Mapping, List

from .types import Coro, TypeCache
from ..objects.message.context import MessageContext


def should_pass_cls(call: Union[Coro, Callable[[Any], Any]]) -> bool:
    """
    Checks whether a callable requires a self/cls as first parameter.

    Parameters
    ----------
    call: Union[Coro, Callable[[Any], Any]]
        The callable to check.

    Returns
    -------
    bool
        Whether the callable requires a self/cls as first parameter.
    """
    args = getfullargspec(call).args
    return len(args) >= 1 and args[0] in ["self", "cls"]


def should_pass_gateway(call: Union[Coro, Callable[[Any], Any]]) -> bool:
    """
    Checks whether a callable requires a dispatcher as last parameter.

    Parameters
    ----------
    call: Union[:class:`~pincer.utils.types.Coro`, Callable[[Any], Any]]
        The callable to check.

    Returns
    -------
    bool
        Whether the callable requires a dispatcher as first parameter.
    """
    args = getfullargspec(call).args
    return len(args) >= 2 and args[1] in ("gateway", "shard")


context_types = [Signature.empty, MessageContext]


def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool:
    # TODO: Fix docs
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

    return annotation == MessageContext or params[0] == "ctx"
