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
from inspect import getfullargspec, Parameter, Signature
from typing import Any, Union, Callable, Mapping, List

from ..objects.context import Context
from .types import Coro


def should_pass_cls(call: Union[Coro, Callable[..., Any]]) -> bool:
    """
    Checks whether a callable requires a self/cls as first parameter.

    :param call:
        The callable to check.

    :return:
        Whether or not its required.
    """
    args = getfullargspec(call).args
    return len(args) >= 1 and args[0] in ["self", "cls"]


context_types = [Signature.empty, Context]


def should_pass_ctx(sig: Mapping[str, Parameter], params: List[str]) -> bool:
    # TODO: Write docs
    return len(params) >= 1 and sig[params[0]].annotation in context_types
