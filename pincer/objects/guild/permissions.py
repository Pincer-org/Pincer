# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag
from typing import Tuple, Optional


class PermissionEnum(IntFlag):
    """
    Represents the permissions for a guild.
    """

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
class Permissions:
    """
    Allows for easier access to the permissions

    Parameters
    ----------
    create_instant_invite: :class:Optional[:class:`bool`]
        Allows creation of instant invites
    kick_members: :class:Optional[:class:`bool`]
        Allows kicking members
    ban_members: :class:Optional[:class:`bool`]
        Allows banning members
    administrator: :class:Optional[:class:`bool`]
        Allows all permissions and bypasses channel permission overwrites
    manage_channels: :class:Optional[:class:`bool`]
        Allows management and editing of channels
    manage_guild: :class:Optional[:class:`bool`]
        Allows management and editing of the guild
    add_reactions: :class:Optional[:class:`bool`]
        Allows for the addition of reactions to messages
    view_audit_log: :class:Optional[:class:`bool`]
        Allows for viewing of audit logs
    priority_speaker: :class:Optional[:class:`bool`]
        Allows for using priority speaker in a voice channel
    stream: :class:Optional[:class:`bool`]
        Allows the user to go live
    view_channel: :class:Optional[:class:`bool`]
        Allows guild members to view a channel, which includes reading messages in text channels
    send_messages: :class:Optional[:class:`bool`]
        Allows for sending messages in a channel (does not allow sending messages in threads)
    send_tts_messages: :class:Optional[:class:`bool`]
        Allows for sending of tts messages
    manage_messages: :class:Optional[:class:`bool`]
        Allows for deletion of other users messages
    embed_links: :class:Optional[:class:`bool`]
        Links sent by users with this permission will be auto-embedded
    attach_files: :class:Optional[:class:`bool`]
        Allows for uploading images and files
    read_message_history: :class:Optional[:class:`bool`]
        Allows for reading of message history
    mention_everyone: :class:Optional[:class:`bool`]
        Allows for using the @everyone tag to notify all users in a channel, and the @here tag to notify all online users in a channel
    use_external_emojis: :class:Optional[:class:`bool`]
        Allows the usage of custom emojis from other servers
    view_guild_insights: :class:Optional[:class:`bool`]
        Allows for viewing of guild insights
    connect: :class:Optional[:class:`bool`]
        Allows for joining of a voice channel
    speak: :class:Optional[:class:`bool`]
        Allows for speaking in a voice channel
    mute_members: :class:Optional[:class:`bool`]
        Allows for muting members in a voice channel
    deafen_members: :class:Optional[:class:`bool`]
        Allows for deafening of members in a voice channel
    move_members: :class:Optional[:class:`bool`]
        Allows for moving of members between voice channels
    use_vad: :class:Optional[:class:`bool`]
        Allows for using voice activity detection in a voice channel
    change_nickname: :class:Optional[:class:`bool`]
        Allows for modification of own nickname
    manage_nicknames: :class:Optional[:class:`bool`]
        Allows for modification of other users nicknames
    manage_roles: :class:Optional[:class:`bool`]
        Allows for management and editing of roles
    manage_webhooks: :class:Optional[:class:`bool`]
        Allows for management and editing of webhooks
    manage_emojis_and_stickers: :class:Optional[:class:`bool`]
        Allows for management and editing of emojis and stickers
    use_application_commands: :class:Optional[:class:`bool`]
        Allows for using application-specific commands
    request_to_speak: :class:Optional[:class:`bool`]
        Allows for requesting to speak in a voice channel
    manage_events: :class:Optional[:class:`bool`]
        Allows for management and editing of events
    manage_threads: :class:Optional[:class:`bool`]
        Allows for management and editing of threads
    create_public_threads: :class:Optional[:class:`bool`]
        Allows for the creation of public threads
    create_private_threads: :class:Optional[:class:`bool`]
        Allows for the creation of private threads
    use_external_stickers: :class:Optional[:class:`bool`]
        Allows for the usage of stickers from other servers
    send_messages_in_threads: :class:Optional[:class:`bool`]
        Allows for sending messages in threads
    start_embedded_activities: :class:Optional[:class:`bool`]
        Allows for starting of embedded activities
    moderate_members: :class:Optional[:class:`bool`]
        Allows for moderation of members in a guild
    """

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

    @classmethod
    def from_ints(cls, allow: int, deny: int) -> Permissions:
        """
        Create a Permission object from an integer representation of the permissions (deny and allow)

        Parameters
        ----------
        allow: :class:`int`
            The integer representation of the permissions that are allowed
        deny: :class:`int`
            The integer representation of the permissions that are denied
        """
        clsobj = cls()

        for enum in PermissionEnum:
            value = None
            if enum.value & allow:
                value = True
            elif enum.value & deny:
                value = False

            setattr(clsobj, enum.name.lower(), value)

        return clsobj

    def to_ints(self) -> Tuple[int]:
        """
        Convert the Permission object to an integer representation of the permissions (deny and allow)

        Returns
        -------
        :class:`Tuple[:class:`int`]`
            The integer representation of the permissions that are allowed and denied
        """
        allow = 0
        deny = 0
        for enum in PermissionEnum:
            if getattr(self, enum.name.lower()):
                allow |= enum.value
            elif getattr(self, enum.name.lower()) is False:
                deny |= enum.value

        return allow, deny

    @property
    def allow(self) -> int:
        """
        Returns the integer representation of the permissions that are allowed
        """
        allow = 0
        for enum in PermissionEnum:
            if getattr(self, enum.name.lower()):
                allow |= enum.value

        return allow

    @property
    def deny(self) -> int:
        """
        Returns the integer representation of the permissions that are denied
        """
        deny = 0
        for enum in PermissionEnum:
            if getattr(self, enum.name.lower()) is False:
                deny |= enum.value

        return deny
