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
from typing import Optional, List

from .user import User
from ..utils import APIObject, APINullable, MISSING, Snowflake


@dataclass
class Application(APIObject):
    """
    Represents a Discord application. (eg Bot, OAuth)

    :param bot_public:
        when false only app owner can join the app's bot to guilds

    :param bot_require_code_grant:
        when true the app's bot will only join upon completion of the
        full oauth2 code grant flow

    :param description:
        the description of the app

    :param id:
        the id of the app

    :param icon:
        the icon hash of the app

    :param name:
        the name of the app

    :param privacy_policy_url:
        the url of the app's privacy policy

    :param summary:
        if this application is a game sold on Discord, this field will be the
        summary field for the store page of its primary sku

    :param verify_key:
        the hex encoded key for verification in interactions and the GameSDK's
        GetTicket

    :param cover_image:
        the application's default rich presence invite cover image hash

    :param flags:
        the application's public flags

    :param guild_id:
        if this application is a game sold on Discord, this field will be the
        guild to which it has been linked

    :param owner:
        partial user object containing info on the owner of the application

    :param primary_sku_id:
        if this application is a game sold on Discord, this field will be the
        id of the "Game SKU" that is created, if exists

    :param rpc_origins:
        an array of rpc origin urls, if rpc is enabled

    :param slug:
        if this application is a game sold on Discord, this field will be the
        URL slug that links to the store page

    :param terms_of_service_url:
        the url of the app's terms of service
    """

    bot_public: bool
    bot_require_code_grant: bool
    description: str
    id: Snowflake
    icon: Optional[str]
    name: str
    privacy_policy_url: APINullable[str]
    summary: str
    verify_key: str

    cover_image: APINullable[str] = MISSING
    flags: APINullable[int] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    owner: APINullable[User] = MISSING
    primary_sku_id: APINullable[Snowflake] = MISSING
    rpc_origins: APINullable[List[str]] = MISSING
    slug: APINullable[str] = MISSING
    terms_of_service_url: APINullable[str] = MISSING
