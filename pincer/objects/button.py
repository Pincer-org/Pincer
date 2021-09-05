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
from enum import Enum

from pincer.objects.emoji import Emoji
from pincer.utils.constants import OptionallyProvided

class ButtonStyle(Enum):
	"""
	Buttons come in a variety of styles to convey different types of actions.
	These styles also define what fields are valid for a button.

	Primary:
		- color: blurple
		- required_field: custom_id
	Secondary:
		- color: gray
		- required_field: custom_id
	Success:
		- color: green
		- required_field: custom_id
	Danger:
		- color: red
		- required_field: custom_id
	Link:
		- color: gray, navigates to a URL
		- required_field: url
	"""
	PRIMARY = 1
	SECONDARY = 2
	SUCCESS = 3
	DANGER = 4
	LINK = 5

@dataclass
class Button:
	"""
	Represents a Discord Button object. Buttons are interactive components
	that render on messages. They can be clicked by users, and send an
	interaction to your app when clicked.
	
	:param type: `2` for a button
	:param style: one of button styles
	:param label: text that appears on the button, max 80 characters
	:param emoji: `name`, `id`, and `animated`
	:param custom_id: a developer-defined identifier for the button, max 100 characters
	:param url: a url for link-style buttons
	:param disabled: whether the button is disabled (default `False`)
	"""
	type: int
	style: ButtonStyle

	label: OptionallyProvided[str] = MISSING
	emoji: OptionallyProvided[Emoji] = MISSING
	custom_id: OptionallyProvided[str] = MISSING
	url: OptionallyProvided[str] = MISSING
	disabled: OptionallyProvided[bool] = False
