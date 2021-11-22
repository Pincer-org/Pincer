# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from inspect import getfullargspec
from typing import TYPE_CHECKING

from .types import T, MISSING

if TYPE_CHECKING:
    from ..client import Client
    from typing import Dict, Callable, Any, Optional


def construct_client_dict(client: Client, data: Dict[...]):
    # TODO: fix docs
    """

    Parameters
    ----------
    client
    data

    Returns
    -------

    """
    return {**data, "_client": client, "_http": client.http}


def convert(
    value: Any,
    factory: Callable[[Any], T],
    check: Optional[T] = None,
    client: Optional[Client] = None,
) -> T:
    """
    Parameters
    ----------
    value : Any
        The value that has to have its type converted.
    factory : Callable[[Any], T]
        The conversion factory/object to use.
    check : Optional[T]
        Skip conversion if ``value`` is already this type.
    client : Optional[:class:`~pincer.client.Client`]
        Reference to :class:`~pincer.client.Client`
    """
    def handle_factory() -> T:
        if check is not None and isinstance(value, check):
            return value

        try:
            if client and "_client" in getfullargspec(factory).args:
                return factory(construct_client_dict(client, value))
        except TypeError:  # Building type/has no signature
            pass

        return factory(value)

    return MISSING if value is MISSING else handle_factory()
