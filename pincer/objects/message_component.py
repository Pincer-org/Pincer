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
from dataclasses import dataclass
from typing import List

from pincer.objects.button import ButtonStyle
from pincer.objects.emoji import Emoji
from pincer.objects.select_menu import SelectOption
from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, APINullable


@dataclass
class MessageComponent(APIObject):
    """
    Represents a Discord Message Component object

    :param type:
        component type

    :param custom_id:
        a developer-defined identifier for the component,
        max 100 characters

    :param disabled:
        whether the component is disabled,
        defaults to `False`

    :param style:
        one of button styles

    :param label:
        text that appears on the button, max 80 characters

    :param emoji:
        `name`, `id`, and `animated`

    :param url:
        a url for link-style buttons

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

    :param components:
        a list of child components
    """
    type: int
    options: List[SelectOption]

    custom_id: APINullable[str] = MISSING
    disabled: APINullable[bool] = False
    style: APINullable[ButtonStyle] = MISSING
    label: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    url: APINullable[str] = MISSING
    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    components: APINullable[List[MessageComponent]] = MISSING
