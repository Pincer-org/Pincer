# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from inspect import signature

from .insertion import should_pass_cls
from .types import Coro


def get_signature_and_params(func: Coro):
    """
    Get the signature and its parameters from a coroutine.

    :param func:
        The coroutine from whom the information should be extracted.
    """
    sig = signature(func).parameters
    params = list(sig)

    if should_pass_cls(func):
        del params[0]

    return sig, params


def get_params(func: Coro):
    """
    Get the parameters from a coroutine.

    :param func:
        The coroutine from whom the information should be extracted.
    """
    return get_signature_and_params(func)[1]
