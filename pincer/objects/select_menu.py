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

from dataclasses import dataclass
from typing import List

from pincer.objects.emoji import Emoji
from pincer.utils.api_object import APIObject
from pincer.utils.types import MISSING, APINullable


@dataclass
class SelectOption(APIObject):
    """
    Represents a Discord Select Option object

    :param label:
        the user-facing name of the option, max 100 characters

    :param value:
        the def-defined value of the option, max 100 characters

    :param description:
        an additional description of the option, max 100 characters

    :param emoji:
        `id`, `name`, and `animated`

    :param default:
        will render this option as selected by default
    """
    label: str
    value: str
    description: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    default: APINullable[bool] = MISSING


@dataclass
class SelectMenu(APIObject):
    """
    Represents a Discord Select Menu object

    :param type:
        `3` for a select menu

    :param custom_id:
        a developer-defined identifier for the button,
        max 100 characters

    :param options:
        the choices in the select, max 25

    :param placeholder:
        custom placeholder text if nothing is selected,
        max 100 characters

    :param min_values:
        the minimum number of items that must be chosen;
        default 1, min 0, max 25

    :param max_values:
        the maximum number of items that can be chosen;
         default 1, max 25

    :param disabled:
        disable the select, default False
    """
    type: int
    custom_id: str
    options: List[SelectOption]

    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    disabled: APINullable[bool] = False
