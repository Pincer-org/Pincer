# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Guild events"""

from __future__ import annotations
from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import (
    GuildBanAddEvent,
    GuildBanRemoveEvent,
    GuildEmojisUpdateEvent,
    GuildIntegrationsUpdateEvent,
    GuildMemberAddEvent,
    GuildMemberRemoveEvent,
    GuildMemberUpdateEvent,
    GuildMembersChunkEvent,
    GuildRoleCreateEvent,
    GuildRoleDeleteEvent,
    GuildRoleUpdateEvent,
    GuildStatusEvent,
    GuildStickersUpdateEvent,
)
from ..utils import Coro
from ..objects import Guild, Channel
from ..utils.conversion import construct_client_dict
from ..objects.guild import Guild, UnavailableGuild

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple
    from ..core.dispatch import GatewayDispatch


async def guild_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_create``,
        generate the guild class that was created

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild create event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.Guild`]]

        ``on_guild_create`` and a ``Guild``
    """
    guild = Guild.from_dict(construct_client_dict(self, payload.data))
    self.guilds[guild.id] = guild
    return "on_guild_create", [guild]


async def guild_ban_add_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_ban_add`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild ban add event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildBaAddEvent`]]
        ``on_guild_ban_add_update`` and a ``GuildBanAddEvent``
    """

    return (
        "on_guild_ban_add",
        [GuildBanAddEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_unban_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_ban_remove`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild ban remove event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildBanRemoveEvent`]]
        ``on_guild_ban_remove_update`` and a ``GuildBanRemoveEvent``
    """

    return (
        "on_guild_ban_remove",
        [GuildBanRemoveEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_delete`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.guild.UnavailableGuild`]]
        ``on_guild_delete`` and an ``UnavailableGuild``
    """
    guild = UnavailableGuild.from_dict(construct_client_dict(self, payload.data))

    if guild.id in self.guilds.key():
        self.guilds.pop(guild.id)

    return "on_guild_delete", [guild]


async def guild_emojis_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_emojis_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild emojis update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildEmojisUpdateEvent`]]
        ``on_guild_emoji_update`` and a ``GuildEmojisUpdateEvent``
    """

    return (
        "on_guild_emojis_update",
        [GuildEmojisUpdateEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_integrations_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_integrations_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild integrations update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildIntegrationsUpdateEvent`]]
        ``on_guild_integration_update`` and a ``GuildIntegrationsUpdateEvent``
    """

    return (
        "on_guild_integrations_update",
        [
            GuildIntegrationsUpdateEvent.from_dict(
                construct_client_dict(self, payload.data)
            )
        ],
    )


async def guild_member_add_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_add`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member add event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberAddEvent`]]
        ``on_guild_member_add`` and a ``GuildMemberAddEvent``
    """

    return "on_guild_member_add", [
        GuildMemberAddEvent.from_dict(construct_client_dict(self, payload.data))
    ]


async def guild_member_remove_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_remove`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member remove event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberRemoveEvent`]]
        ``on_guild_member_remove`` and a ``GuildMemberRemoveEvent``
    """

    return (
        "on_guild_member_remove",
        [GuildMemberRemoveEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_member_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberUpdateEvent`]]
        ``on_guild_member_update`` and a ``GuildMemberUpdateEvent``
    """

    return (
        "on_guild_member_update",
        [GuildMemberUpdateEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_member_chunk_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_chunk`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member chunk event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberChunkEvent`]]
        ``on_guild_member_chunk`` and a ``GuildMemberChunkEvent``
    """

    return (
        "on_guild_member_chunk",
        [GuildMembersChunkEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_role_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_role_create`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild role create event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildRoleCreateEvent`]]
        ``on_guild_role_create`` and a ``GuildRoleCreateEvent``
    """

    return (
        "on_guild_role_create",
        [GuildRoleCreateEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_role_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_role_delete`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild role delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildRoleDeleteEvent`]]
        ``on_guild_role_delete`` and a ``GuildRoleDeleteEvent``
    """

    return (
        "on_guild_role_delete",
        [GuildRoleDeleteEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.guild.Guild`]]
        ``on_guild_Update`` and an ``Guild``
    """

    channel_list = payload.data.pop("channels", [])

    channels: List[Channel] = [
        Channel.from_dict(construct_client_dict(self, channel))
        for channel in channel_list
    ]

    guild = Guild.from_dict(
        construct_client_dict(self, {"channels": channels, **payload.data})
    )
    self.guild[guild.id] = guild

    return "on_guild_update", [guild]


async def guild_stickers_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_stickers_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild stickers update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildStickersUpdateEvent`]]
        ``on_guild_sticker_update`` and a ``GuildStickersUpdateEvent``
    """

    return (
        "on_guild_stickers_update",
        [GuildStickersUpdateEvent.from_dict(construct_client_dict(self, payload.data))],
    )


async def guild_status_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_status`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild status event.

    Return
    ------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildStatusEvent`]]
        ``on_guild_status`` and a ``GuildStatusEvent``
    """
    return "on_guild_status", [
        GuildStatusEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return (
        guild_ban_add_middleware,
        guild_unban_middleware,
        guild_create_middleware,
        guild_delete_middleware,
        guild_emojis_update_middleware,
        guild_member_add_middleware,
        guild_integrations_update_middleware,
        guild_member_remove_middleware,
        guild_member_update_middleware,
        guild_members_chunk_middleware,
        guild_role_create_middleware,
        guild_update_middleware,
        guild_stickers_update_middleware,
        guild_status_middleware,
    )
