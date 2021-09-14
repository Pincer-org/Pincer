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

from pincer.utils.api_object import APIObject
from pincer.utils.snowflake import Snowflake
from pincer.utils.types import MISSING, APINullable


@dataclass
class IntegrationDeleteEvent(APIObject):
    """
    Sent when an integration is deleted.

    :param id:
        integration id

    :param guild_id:
        id of the guild

    :param application_id:
        id of the bot/OAuth2 application for this discord integration
    """
    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake] = MISSING
