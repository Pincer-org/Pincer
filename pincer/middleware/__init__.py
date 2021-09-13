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

from typing import Dict

from pincer.utils import Coro
from .interaction_create import interaction_create_middleware
from .ready import on_ready_middleware

# TODO: Make imports dynamic.
# from glob import glob
# from importlib import import_module
# from os import path
# from pathlib import Path
# from pincer.exceptions import NoExportMethod

# def get_middleware() -> Dict[str, Coro]:
#     middleware_list: Dict[str, Coro] = {}
#
#     for middleware_path in glob(path.join(
#             Path(__file__).parent.resolve(),
#             "[!__init__]*.py")
#     ):
#         event = middleware_path[:-3]
#
#         try:
#             middleware_list[event] = getattr(import_module(f"event"), "export")
#         except AttributeError:
#             raise NoExportMethod(
#                 f"Middleware module `{middleware_path}` expected an "
#                 "`export` method but none was found!"
#             )
#
#     return middleware_list
# middleware: Dict[str, Coro] = get_middleware()

middleware: Dict[str, Coro] = {
    "ready": on_ready_middleware,
    "interaction_create": interaction_create_middleware
}
