# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List, Set, Union, Tuple


def remove_none(
    obj: Union[List, Dict, Set, Tuple]
) -> Union[List, Dict, Set, Tuple]:
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
