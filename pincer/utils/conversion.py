# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from inspect import getfullargspec
from typing import TYPE_CHECKING

from .types import T, MISSING

if TYPE_CHECKING:
    from ..client import Client
    from typing import Any, Callable, Dict, List, Optional, Set, Union


def construct_client_dict(client: Client, data: Dict) -> Dict:
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


def remove_none(obj: Union[List, Dict, Set]) -> Union[List, Dict, Set]:
    """
    Removes all ``None`` values from a list, dict or set.

    Parameters
    ----------
    obj : Union[List, Dict, Set]
        The list, dict or set to remove ``None`` values from.

    Returns
    -------
    Union[List, Dict, Set]
        The list, dict or set without ``None`` values.
    """
    if isinstance(obj, list):
        return [i for i in obj if i is not None]
    elif isinstance(obj, set):
        return obj - {None}
    elif isinstance(obj, dict):
        return {k: v for k, v in obj.items() if None not in {k, v}}
