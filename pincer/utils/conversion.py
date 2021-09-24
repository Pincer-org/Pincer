# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
            return (
                v if check is not None and isinstance(v, check)
                else factory(v) if client is None
                else factory(v | {"_client": client, "_http": client.http})
            )

        return (
            list(map(fin_fac, value))
            if isinstance(value, list)
            else fin_fac(value)
        )

    return MISSING if value is MISSING else handle_factory()
