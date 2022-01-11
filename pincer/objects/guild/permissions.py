# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, Optional


class Permissions(Enum):
    CREATE_INSTANT_INVITE = 1 << 0
    KICK_MEMBERS = 1 << 1
    BAN_MEMBERS = 1 << 2
    ADMINISTRATOR = 1 << 3
    MANAGE_CHANNELS = 1 << 4
    MANAGE_GUIlD = 1 << 5
    ADD_REACTIONS = 1 << 6
    VIEW_AUDIT_LOG = 1 << 7
    PRIORITY_SPEAKER = 1 << 8
    STREAM = 1 << 9
    VIEW_CHANNEL = 1 << 10
    SEND_MESSAGES = 1 << 11
    SEND_TTS_MESSAGES = 1 << 12
    MANAGE_MESSAGES = 1 << 13
    EMBED_LINKS = 1 << 14
    ATTACH_FILES = 1 << 15
    READ_MESSAGE_HISTORY = 1 << 16
    MENTION_EVERYONE = 1 << 17
    USE_EXTERNAL_EMOJIS = 1 << 18
    VIEW_GUILD_INSIGHTS = 1 << 19
    CONNECT = 1 << 20
    SPEAK = 1 << 21
    MUTE_MEMBERS = 1 << 22
    DEAFEN_MEMBERS = 1 << 23
    MOVE_MEMBERS = 1 << 24
    USE_VAD = 1 << 25
    CHANGE_NICKNAME = 1 << 26
    MANAGE_NICKNAMES = 1 << 27
    MANAGE_ROLES = 1 << 28
    MANAGE_WEBHOOKS = 1 << 29
    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    USE_APPLICATION_COMMANDS = 1 << 31
    REQUEST_TO_SPEAK = 1 << 32
    MANAGE_EVENTS = 1 << 33
    MANAGE_THREADS = 1 << 34
    CREATE_PUBLIC_THREADS = 1 << 35
    CREATE_PRIVATE_THREADS = 1 << 36
    USE_EXTERNAL_STICKERS = 1 << 37
    SEND_MESSAGES_IN_THREADS = 1 << 38
    START_EMBEDDED_ACTIVITIES = 1 << 39
    MODERATE_MEMBERS = 1 << 40


@dataclass
class Permission:
    create_instant_invite: Optional[bool] = None
    kick_members: Optional[bool] = None
    ban_members: Optional[bool] = None
    administrator: Optional[bool] = None
    manage_channels: Optional[bool] = None
    manage_guild: Optional[bool] = None
    add_reactions: Optional[bool] = None
    view_audit_log: Optional[bool] = None
    priority_speaker: Optional[bool] = None
    stream: Optional[bool] = None
    view_channel: Optional[bool] = None
    send_messages: Optional[bool] = None
    send_tts_messages: Optional[bool] = None
    manage_messages: Optional[bool] = None
    embed_links: Optional[bool] = None
    attach_files: Optional[bool] = None
    read_message_history: Optional[bool] = None
    mention_everyone: Optional[bool] = None
    use_external_emojis: Optional[bool] = None
    view_guild_insights: Optional[bool] = None
    connect: Optional[bool] = None
    speak: Optional[bool] = None
    mute_members: Optional[bool] = None
    deafen_members: Optional[bool] = None
    move_members: Optional[bool] = None
    use_vad: Optional[bool] = None
    change_nickname: Optional[bool] = None
    manage_nicknames: Optional[bool] = None
    manage_roles: Optional[bool] = None
    manage_webhooks: Optional[bool] = None
    manage_emojis_and_stickers: Optional[bool] = None
    use_application_commands: Optional[bool] = None
    request_to_speak: Optional[bool] = None
    manage_events: Optional[bool] = None
    manage_threads: Optional[bool] = None
    create_public_threads: Optional[bool] = None
    create_private_threads: Optional[bool] = None
    use_external_stickers: Optional[bool] = None
    send_messages_in_threads: Optional[bool] = None
    start_embedded_activities: Optional[bool] = None
    moderate_members: Optional[bool] = None

    def __setattr__(self, name: str, value: Optional[bool]) -> None:
        if not isinstance(value, bool) and value is not None:
            raise ValueError(f"Permission {name!r} must be a boolean or None")
        return super().__setattr__(name, value)

    def __eq__(self, object) -> bool:
        """
        Permission equality is determined by comparing the integer values of the permissions
        """
        if isinstance(object, Permission):
            return self.to_int() == object.to_int()
        elif isinstance(object, tuple):
            return self.to_int() == object

        return False

    @classmethod
    def from_int(cls, allow: int, deny: int) -> Permission:
        clsobj = cls()

        for enum in Permissions:
            if bool(enum.value & allow):
                setattr(clsobj, enum.name.lower(), True)
            elif bool(enum.value & deny):
                setattr(clsobj, enum.name.lower(), False)
            else:
                setattr(clsobj, enum.name.lower(), None)

        return clsobj

    def to_int(self) -> Tuple[int]:
        allow = 0
        deny = 0
        for enum in Permissions:
            if getattr(self, enum.name.lower()):
                allow |= enum.value
            elif getattr(self, enum.name.lower()) is False:
                deny |= enum.value

        return allow, deny

    @property
    def allow(self) -> int:
        allow = 0
        for enum in Permissions:
            if getattr(self, enum.name.lower()):
                allow |= enum.value

        return allow

    @property
    def deny(self) -> int:
        deny = 0
        for enum in Permissions:
            if getattr(self, enum.name.lower()) is False:
                deny |= enum.value

        return deny
