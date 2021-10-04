# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from inspect import signature, isclass
from typing import Callable

from .insertion import should_pass_cls


def get_signature_and_params(func: Callable):
    """
    Get the signature and its parameters from a coroutine.

    :param func:
        The coroutine from whom the information should be extracted.
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
    """
    Get the parameters from a coroutine.

    :param func:
        The coroutine from whom the information should be extracted.
    """
    return get_signature_and_params(func)[1]
