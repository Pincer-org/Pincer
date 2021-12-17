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
    return {**data, "_client": client}


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
