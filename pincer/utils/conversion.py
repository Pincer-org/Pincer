# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from inspect import getfullargspec
from typing import TYPE_CHECKING

from .types import T, MISSING

if TYPE_CHECKING:
    from ..client import Client
    from typing import Any, Callable, Dict, List, Optional, Set, Union, Tuple


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
    return {**data, "_client": client}


def remove_none(obj: Union[List, Dict, Set, Tuple]) -> Union[List, Dict, Set, Tuple]:
    """
    Removes all ``None`` values from a list, dict or set.

    Parameters
    ----------
    obj : Union[List, Dict, Set, Tuple]
        The list, dict, set or tuple to remove ``None`` values from.

    Returns
    -------
    Union[List, Dict, Set, Tuple]
        The list, dict, set or tuple, without ``None`` values.
    """
    if isinstance(obj, list):
        return [i for i in obj if i is not None]
    elif isinstance(obj, tuple):
        return tuple(i for i in obj if i is not None)
    elif isinstance(obj, set):
        return obj - {None}
    elif isinstance(obj, dict):
        return {k: v for k, v in obj.items() if None not in (k, v)}


def dict_to_query(data: Dict[str, Any]) -> str:
    """
    Takes a dictionary of arguments and converts it into a query string to append to a url.

    Parameters
    ----------
    data : Dict[:class:`str`, :class:`~typing.Any`]
        The arguments for the query string

    Returns
    -------
    str
        The query string to append to a url
    """
    query_str = ""
    for key in data:
        if data[key] is not None:
            query_str += f"{key}={data[key]}&"
    return query_str[:-1]
