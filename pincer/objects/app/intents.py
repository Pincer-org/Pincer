# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum


class Intents(IntEnum):
    """Discord client intents.

    These give your client more permissions.

    .. note::
        The given Intents must also be enabled for your client on
        the discord dashboard.

    Attributes
    ----------
    NONE:
        No intents.
    GUILDS:
        Guilds intent.
    GUILD_MEMBERS:
        Members intent.
    GUILD_BANS:
        Bans intent.
    GUILD_EMOJIS_AND_STICKERS:
        Emoji and Sticker intent.
    GUILD_INTEGRATIONS:
        Integrations intent.
    GUILD_WEBHOOKS:
        Webhooks intent.
    GUILD_INVITES:
        Invites intent.
    GUILD_VOICE_STATES:
        Voice states intent.
    GUILD_PRESENCES:
        Presences intent.
    GUILD_MESSAGES:
        Message intent.
    GUILD_MESSAGE_REACTIONS:
        Reactions to messages intent.
    GUILD_MESSAGE_TYPING:
        Typing to messages intent.
    DIRECT_MESSAGES:
        DM messages intent.
    DIRECT_MESSAGE_REACTIONS:
        DM reaction to messages intent.
    DIRECT_MESSAGE_TYPING:
        DM typing to messages intent.
    """
    NONE = 0
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14

    @staticmethod
    def all() -> int:
        """
        :class:`~pincer.objects.app.intents.Intents`:
        Method of all intents
        """
        res = 0

        for intent in list(map(lambda itm: itm.value, Intents)):
            res |= intent

        return res
