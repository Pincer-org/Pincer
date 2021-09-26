# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import Callable, Any, Optional, TYPE_CHECKING
from .types import T, MISSING

if TYPE_CHECKING:
    from pincer.client import Client


def convert(
        value: Any,
        factory: Callable[[Any], T],
        check: Optional[type] = None,
        client: Optional[Client] = None
) -> T:
    """
    Convert a value to T if its not MISSING.
    """
    def handle_factory() -> T:
        def fin_fac(v: Any):
            if check is not None and isinstance(v, check):
                return v

            if client is None:
                return factory(v)

            return factory({**v, "_client": client, "_http": client.http})

        return (
            list(map(fin_fac, value))
            if isinstance(value, list)
            else fin_fac(value)
        )

    return MISSING if value is MISSING else handle_factory()
