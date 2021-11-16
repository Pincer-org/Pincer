# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from inspect import signature, isclass
from typing import Callable

from .insertion import should_pass_cls


def get_signature_and_params(func: Callable):
    """Get the parameters and signature from a coroutine.

    func: Callable
        The coroutine from whom the information should be extracted.

    Returns
    -------
    Tuple[List[Union[:class:`str`, :class:`inspect.Parameter`]]]
        Signature and ist of parameters of the coroutine.
    """
    if isclass(func):
        func = getattr(func, "__init__")

        if func is object.__init__:
            return [], []

    sig = signature(func).parameters
    params = list(sig)

    if should_pass_cls(func):
        del params[0]

    return sig, params


def get_params(func: Callable):
    """Get the parameters from a coroutine.

    func: Callable
        The coroutine from whom the information should be extracted.

    Returns
    -------
    List[Union[:class:`str`, :class:`inspect.Parameter`]]
        List of parameters of the coroutine.
    """
    return get_signature_and_params(func)[1]
