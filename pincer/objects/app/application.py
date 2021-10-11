# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from ...utils.api_object import APIObject
from ...utils.types import MISSING
from ...utils import snowflake
from ...utils import types
from ..user.user import User


@dataclass
class Application(APIObject):
    """Represents a Discord application. (eg Bot, OAuth)

    Attributes
    ----------
    bot_public: :class:`bool`
        when false only app owner can join the app's bot to guilds
    bot_require_code_grant: :class:`bool`
        when true the app's bot will only join upon completion of the
        full oauth2 code grant flow
    description: :class:`str`
        the description of the app
    id: :class:`~pincer.utils.snowflake.Snowflake`
        the id of the app
    icon: :data:`~typing.Optional`\\[:class:`str`]
        the icon hash of the app
    name: :class:`str`
        the name of the app
    privacy_policy_url: :data:`~pincer.utils.types.APINullable`\\[:class:`str`]
        the url of the app's privacy policy
    summary: :class:`str`
        if this application is a game sold on Discord, this field will be the
        summary field for the store page of its primary sku
    verify_key: :class:`str`
        the hex encoded key for verification in interactions and the GameSDK's
        GetTicket
    cover_image: :data:`~pincer.utils.types.APINullable`\\[:class:`str`]
        the application's default rich presence invite cover image hash
    flags: :data:`~pincer.utils.types.APINullable`\\[:class:`int`]
        the application's public flags
    guild_id: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        if this application is a game sold on Discord, this field will be the
        guild to which it has been linked
    owner: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.objects.user.user.User`]
        partial user object containing info on the owner of the application
    primary_sku_id: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        if this application is a game sold on Discord, this field will be the
        id of the "Game SKU" that is created, if exists
    rpc_origins: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.List`\\[:class:`str`]]
        an array of rpc origin urls, if rpc is enabled
    slug: :data:`~pincer.utils.types.APINullable`\\[:class:`str`]
        if this application is a game sold on Discord, this field will be the
        URL slug that links to the store page
    terms_of_service_url: :data:`~pincer.utils.types.APINullable`\\[:class:`str`]
        the url of the app's terms of service
    """
    bot_public: bool
    bot_require_code_grant: bool
    description: str
    id: snowflake.Snowflake
    icon: Optional[str]
    name: str
    privacy_policy_url: types.APINullable[str]
    summary: str
    verify_key: str

    cover_image: types.APINullable[str] = MISSING
    flags: types.APINullable[int] = MISSING
    guild_id: types.APINullable[snowflake.Snowflake] = MISSING
    owner: types.APINullable[User] = MISSING
    primary_sku_id: types.APINullable[snowflake.Snowflake] = MISSING
    rpc_origins: types.APINullable[List[str]] = MISSING
    slug: types.APINullable[str] = MISSING
    terms_of_service_url: types.APINullable[str] = MISSING
