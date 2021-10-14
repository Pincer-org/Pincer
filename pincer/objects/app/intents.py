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
    """
    NONE = 0  #: No intents
    GUILDS = 1 << 0  #: Guilds intent
    GUILD_MEMBERS = 1 << 1  #: Members intent
    GUILD_BANS = 1 << 2  #: Ban intent
    GUILD_EMOJIS_AND_STICKERS = 1 << 3  #: Emoji and sticker intent
    GUILD_INTEGRATIONS = 1 << 4  #: Integrations intent
    GUILD_WEBHOOKS = 1 << 5  #: Webhooks intent
    GUILD_INVITES = 1 << 6  #: Invites intent
    GUILD_VOICE_STATES = 1 << 7  #: Voice intent
    GUILD_PRESENCES = 1 << 8  #: Presence intent
    GUILD_MESSAGES = 1 << 9  #: Message intent
    GUILD_MESSAGE_REACTIONS = 1 << 10  #: Reactions intent
    GUILD_MESSAGE_TYPING = 1 << 11  #: Typing intent
    DIRECT_MESSAGES = 1 << 12  #: DM intent
    DIRECT_MESSAGE_REACTIONS = 1 << 13  #: DM reactions intent
    DIRECT_MESSAGE_TYPING = 1 << 14  #: DM typing intent

    @staticmethod
    def all() -> Intents:
        """:class:`~pincer.objects.app.intents.Intents`: Method of all intents
        """
        res = 0

        for intent in list(map(lambda itm: itm.value, Intents)):
            res |= intent

        return res
