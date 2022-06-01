# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from asyncio import sleep, ensure_future
from dataclasses import dataclass
from enum import IntEnum
from typing import AsyncIterator, overload, TYPE_CHECKING

from .invite import Invite, InviteTargetType
from ..message.user_message import UserMessage
from ..._config import GatewayConfig
from ...utils.api_data import APIDataGen
from ...utils.api_object import APIObject, GuildProperty
from ...utils.convert_message import convert_message
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Dict, List, Optional, Union

    from .member import GuildMember
    from .overwrite import Overwrite
    from .thread import ThreadMetadata
    from .webhook import Webhook
    from ..message.message import Message
    from ..message.embed import Embed
    from ..user.user import User
    from ...client import Client
    from ...objects import ThreadMember
    from ...utils.timestamp import Timestamp
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


class ChannelType(IntEnum):
    """Represents a channel its type.

    Attributes
    ----------
    GUILD_TEXT:
        A text channel.
    DM:
        A DM channel.
    GUILD_VOICE:
        A voice channel.
    GROUP_DM:
        A group DM channel.
    GUILD_CATEGORY:
        A category channel.
    GUILD_NEWS:
        A news channel.
    GUILD_STORE:
        A store channel.
    GUILD_NEWS_THREAD:
        A news thread.
    GUILD_PUBLIC_THREAD:
        A public thread.
    GUILD_PRIVATE_THREAD:
        A private thread.
    GUILD_STAGE_VOICE:
        A stage channel.
    """

    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6

    if GatewayConfig.version >= 9:
        GUILD_NEWS_THREAD = 10
        GUILD_PUBLIC_THREAD = 11
        GUILD_PRIVATE_THREAD = 12

    GUILD_STAGE_VOICE = 13


@dataclass(repr=False)
class Channel(APIObject, GuildProperty):  # noqa E501
    """Represents a Discord Channel Mention object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of this channel
    type: :class:`~pincer.objects.guild.channel.ChannelType`
        The type of channel
    application_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Application id of the group DM creator if it is bot-created
    bitrate: APINullable[:class:`int`]
        The bitrate (in bits) of the voice channel
    default_auto_archive_duration: APINullable[:class:`int`]
        Default duration for newly created threads, in minutes, to
        automatically archive the thread after recent activity, can be set to:
        60, 1440, 4320, 10080
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild (maybe missing for some channel objects received
        over gateway guild dispatches)
    icon: APINullable[Optional[:class:`str`]]
        Icon hash
    last_message_id: APINullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        The id of the last message sent in this channel (may not point to an
        existing or valid message)
    last_pin_timestamp: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        When the last pinned message was pinned. This may be null in events
        such as GUILD_CREATE when a message is not pinned.
    member: APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
        Thread member object for the current user, if they have joined the
        thread, only included on certain API endpoints
    member_count: APINullable[:class:`int`]
        An approximate count of users in a thread, stops counting at 50
    message_count: :class:`int`
        An approximate count of messages in a thread, stops counting at 50
    name: APINullable[:class:`str`]
        The name of the channel (1-100 characters)
    nsfw: APINullable[:class:`bool`]
        Whether the channel is nsfw
    owner_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the creator of the group DM or thread
    parent_id: APINullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        For guild channels: id of the parent category for a channel (each
        parent category can contain up to 50 channels), for threads: id of the
        text channel this thread was created
    permissions: APINullable[:class:`str`]
        Computed permissions for the invoking user in the channel, including
        overwrites, only included when part of the resolved data received on a
        slash command interaction
    permission_overwrites: APINullable[List[:class:`~pincer.objects.guild.overwrite.Overwrite`]]
        Explicit permission overwrites for members and roles
    position: APINullable[:class:`int`]
        Sorting position of the channel
    rate_limit_per_user: APINullable[:class:`int`]
        Amount of seconds a user has to wait before sending another message
        (0-21600); bots, as well as users with the permission manage_messages
        or manage_channel, are unaffected
    recipients: APINullable[List[:class:`~pincer.objects.user.user.User`]]
        The recipients of the DM
    rtc_region: APINullable[Optional[:class:`str`]]
        Voice region id for the voice channel, automatic when set to null
    thread_metadata: APINullable[:class:`~pincer.objects.guild.thread.ThreadMetadata`]
        Thread-specific fields not needed by other channels
    topic: APINullable[Optional[:class:`str`]]
        The channel topic (0-1024 characters)
    user_limit: APINullable[:class:`int`]
        The user limit of the voice channel
    video_quality_mode: APINullable[:class:`int`]
        The camera video quality mode of the voice channel, 1 when not present
    """

    # noqa: E501
    id: Snowflake
    type: ChannelType

    application_id: APINullable[Snowflake] = MISSING
    bitrate: APINullable[int] = MISSING
    default_auto_archive_duration: APINullable[int] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    icon: APINullable[Optional[str]] = MISSING

    last_message_id: APINullable[Optional[Snowflake]] = MISSING
    last_pin_timestamp: APINullable[Optional[Timestamp]] = MISSING
    member: APINullable[GuildMember] = MISSING

    member_count: APINullable[int] = MISSING

    message_count: APINullable[int] = MISSING

    name: APINullable[str] = MISSING
    nsfw: APINullable[bool] = MISSING
    owner_id: APINullable[Snowflake] = MISSING
    parent_id: APINullable[Optional[Snowflake]] = MISSING
    permissions: APINullable[str] = MISSING
    permission_overwrites: APINullable[List[Overwrite]] = MISSING
    # Position is always 0 when not sent
    position: APINullable[int] = 0
    rate_limit_per_user: APINullable[int] = MISSING
    recipients: APINullable[List[User]] = MISSING
    rtc_region: APINullable[Optional[str]] = MISSING
    thread_metadata: APINullable[ThreadMetadata] = MISSING
    topic: APINullable[Optional[str]] = MISSING
    user_limit: APINullable[int] = MISSING
    video_quality_mode: APINullable[int] = MISSING

    @property
    def mention(self):
        return f"<#{self.id}>"

    @classmethod
    async def from_id(cls, client: Client, channel_id: int) -> Channel:
        """|coro|
        Creates a channel object. You should use the ``get_channel`` method
        from :class:`~pincer.client.Client` most of the time. The
        ``get_dm_channel`` method from :class:`~pincer.objects.user.user.User`
        should be used if you need to create a dm_channel. Using the ``send()``
        method from :class:`~pincer.objects.user.user.User` is preferred.

        Parameters
        ----------
        client : :class:`~pincer.client.Client`
            Client object to use the HTTP class of.
        channel_id : :class:`int`
            ID of the channel you want.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The channel object.
        """
        data = (await client.http.get(f"channels/{channel_id}")) or {}

        data.update({"type": ChannelType(data.pop("type"))})

        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)

    @overload
    async def edit(
        self,
        *,
        name: str = None,
        type: ChannelType = None,
        position: int = None,
        topic: str = None,
        nsfw: bool = None,
        rate_limit_per_user: int = None,
        bitrate: int = None,
        user_limit: int = None,
        permissions_overwrites: List[Overwrite] = None,
        parent_id: Snowflake = None,
        rtc_region: str = None,
        video_quality_mod: int = None,
        default_auto_archive_duration: int = None,
    ) -> Channel:
        ...

    async def edit(self, reason: Optional[str] = None, **kwargs):
        """|coro|
        Edit a channel with the given keyword arguments.

        Parameters
        ----------
        reason Optional[:class:`str`]
            The reason of the channel edit.
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        headers = {}

        if reason is not None:
            headers["X-Audit-Log-Reason"] = str(reason)

        data = await self._http.patch(
            f"channels/{self.id}", kwargs, headers=headers
        )
        data.update({"type": ChannelType(data.pop("type"))})
        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)

    async def edit_permissions(
        self,
        overwrite: Overwrite,
        allow: str,
        deny: str,
        type: int,
        reason: Optional[str] = None,
    ):
        """|coro|
        Edit the channel permission overwrites for a user or role in a channel.
        Only usable for guild channels. Requires the ``MANAGE_ROLES`` permission.
        Only permissions your bot has in the guild or channel can be
        allowed/denied (unless your bot has a ``MANAGE_ROLES`` overwrite in the channel).

        Parameters
        ----------
        overwrite: :class:`~pincer.objects.guild.overwrite.Overwrite`
            The overwrite object.
        allow: :class:`str`
            The bitwise value of all allowed permissions.
        deny: :class:`str`
            The bitwise value of all denied permissions.
        type: :class:`int`
            0 for a role or 1 for a member.
        reason: Optional[:class:`str`]
            The reason of the channel permission edit.
        """
        await self._http.put(
            f"channels/{self.id}/permissions/{overwrite.id}",
            headers={"X-Audit-Log-Reason": reason},
            data={"allow": allow, "deny": deny, "type": type},
        )

    async def delete_permission(
        self, overwrite: Overwrite, reason: Optional[str] = None
    ):
        """|coro|
        Delete a channel permission overwrite for a user or role in a channel.
        Only usable for guild channels. Requires the ``MANAGE_ROLES`` permission.

        Parameters
        ----------
        overwrite: :class:`~pincer.objects.guild.overwrite.Overwrite`
            The overwrite object.
        reason: Optional[:class:`str`]
            The reason of the channel permission delete.
        """
        await self._http.delete(
            f"channels/{self.id}/permissions/{overwrite.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def follow_news_channel(
        self, webhook_channel_id: Snowflake
    ) -> NewsChannel:
        """|coro|
        Follow a News Channel to send messages to a target channel.
        Requires the ``MANAGE_WEBHOOKS`` permission in the target channel.
        Returns a followed channel object.

        Parameters
        ----------
        webhook_channel_id: :class:`Snowflake`
            The ID of the channel to follow.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.NewsChannel`
            The followed channel object.
        """
        return NewsChannel.from_dict(
            self._http.post(
                f"channels/{self.id}/followers",
                data={"webhook_channel_id": webhook_channel_id},
            )
        )

    async def trigger_typing_indicator(self):
        """|coro|
        Post a typing indicator for the specified channel.
        Generally bots should **not** implement this route. However, if a bot is
        responding to a command and expects the computation to take a few
        seconds, this endpoint may be called to let the user know that the bot
        is processing their message.
        """
        await self._http.post(f"channels/{self.id}/typing")

    def get_pinned_messages(self) -> APIDataGen[UserMessage]:
        """|coro|
        Fetches all pinned messages in the channel. Returns an iterator of
        pinned messages.

        Returns
        -------
        :class:`AsyncIterator[:class:`~pincer.objects.guild.message.UserMessage`]`
            An iterator of pinned messages.
        """
        return APIDataGen(
            UserMessage, self._http.get(f"channels/{self.id}/pins")
        )

    async def pin_message(
        self, message: UserMessage, reason: Optional[str] = None
    ):
        """|coro|
        Pin a message in a channel. Requires the ``MANAGE_MESSAGES`` permission.
        The maximum number of pinned messages is ``50``.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason of the channel message pin.
        """
        await self._http.put(
            f"channels/{self.id}/pins/{message.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def unpin_message(
        self, message: UserMessage, reason: Optional[str] = None
    ):
        """|coro|
        Unpin a message in a channel. Requires the ``MANAGE_MESSAGES`` permission.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason of the channel message unpin.
        """
        await self._http.delete(
            f"channels/{self.id}/pins/{message.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def group_dm_add_recipient(
        self,
        user: User,
        access_token: Optional[str] = None,
        nick: Optional[str] = None,
    ):
        """|coro|
        Adds a recipient to a Group DM using their access token.

        Parameters
        ----------
        user: :class:`~pincer.objects.user.User`
            The user to add.
        access_token: Optional[:class:`str`]
            The access token of the user that has granted your app the
            ``gdm.join`` scope.
        nick: Optional[:class:`str`]
            The nickname of the user being added.
        """
        await self._http.put(
            f"channels/{self.id}/recipients/{user.id}",
            data={"access_token": access_token, "nick": nick},
        )

    async def group_dm_remove_recipient(self, user: User):
        """|coro|
        Removes a recipient from a Group DM.

        Parameters
        ----------
        user: :class:`~pincer.objects.user.User`
            The user to remove.
        """
        await self._http.delete(f"channels/{self.id}/recipients/{user.id}")

    async def bulk_delete_messages(
        self, messages: List[Snowflake], reason: Optional[str] = None
    ):
        """|coro|
        Delete multiple messages in a single request.
        This endpoint can only be used on guild channels and requires
        the ``MANAGE_MESSAGES`` permission.

        This endpoint will not delete messages older than 2 weeks, and will
        fail with a 400 BAD REQUEST if any message provided is older than that
        or if any duplicate message IDs are provided.

        Parameters
        ----------
        messages: List[:class:`~.pincer.utils.Snowflake`]
            The list of message IDs to delete (2-100).
        reason: Optional[:class:`str`]
            The reason of the channel bulk delete.
        """
        await self._http.post(
            f"channels/{self.id}/messages/bulk_delete",
            headers={"X-Audit-Log-Reason": reason},
            data={"messages": messages},
        )

    async def delete(
        self,
        reason: Optional[str] = None,
        /,
        channel_id: Optional[Snowflake] = None,
    ):
        """|coro|

        Delete the current channel.

        Parameters
        ----------
        reason Optional[:class:`str`]
            The reason of the channel delete.
        channel_id :class:`~.pincer.utils.Snowflake`
            The id of the channel, defaults to the current object id.
        """
        channel_id = channel_id or self.id

        await self._http.delete(
            f"channels/{channel_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    @staticmethod
    async def __post_send_handler(message: UserMessage):
        """Process a message after it was sent.

        Parameters
        ----------
        message :class:`~.pincer.objects.message.message.Message`
            The message.
        """

        if getattr(message, "delete_after", None):
            await sleep(message.delete_after)
            await message.delete()

    def __post_sent(self, message: UserMessage):
        """Ensure the `__post_send_handler` method its future.

        Parameters
        ----------
        message :class:`~.pincer.objects.message.message.Message`
            The message.
        """
        ensure_future(self.__post_send_handler(message))

    async def send(self, message: Union[Embed, Message, str]) -> UserMessage:
        """|coro|

        Send a message in the channel.

        Parameters
        ----------
        message :class:`~.pincer.objects.message.message.Message`
            The message which must be sent

        Returns
        -------
        :class:`~.pincer.objects.message.user_message.UserMessage`
            The message that was sent.
        """
        content_type, data = convert_message(self._client, message).serialize()

        resp = await self._http.post(
            f"channels/{self.id}/messages", data, content_type=content_type
        )
        msg = UserMessage.from_dict(resp)
        self.__post_sent(msg)
        return msg

    def get_webhooks(self) -> APIDataGen[Webhook]:
        """|coro|
        Get all webhooks in the channel.
        Requires the ``MANAGE_WEBHOOKS`` permission.

        Yields
        -------
        AsyncGenerator[:class:`~.pincer.objects.guild.webhook.Webhook`, None]
        """
        return APIDataGen(
            Webhook, self._http.get(f"channels/{self.id}/webhooks")
        )

    def get_invites(self) -> APIDataGen[Invite]:
        """|coro|
        Fetches all the invite objects for the channel. Only usable for
        guild channels. Requires the ``MANAGE_CHANNELS`` permission.

        Returns
        -------
        AsyncIterator[:class:`~pincer.objects.guild.invite.Invite`]
            Invites iterator.
        """
        return APIDataGen(Invite, self._http.get(f"channels/{self.id}/invites"))

    async def create_invite(
        self,
        max_age: int = 86400,
        max_uses: int = 0,
        temporary: bool = False,
        unique: bool = False,
        target_type: InviteTargetType = None,
        target_user_id: Snowflake = None,
        target_application_id: Snowflake = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Create a new invite object for the channel. Only usable for guild
        channels. Requires the ``CREATE_INSTANT_INVITE`` permission.

        Parameters
        ----------
        max_age: Optional[:class:`int`]
            Duration of invite in seconds before expiry, or 0 for never. between
            0 and 604800 (7 days).
            |default| :data:`86400`
        max_uses: Optional[:class:`int`]
            Maximum number of uses. ``0`` for unlimited. Values between 0 and 100.
            |default| :data:`0`
        temporary: Optional[:class:`bool`]
            Whether the invite only grants temporary membership.
            |default| :data:`False`
        unique: Optional[:class:`bool`]
            If ``True``, don't try to reuse a similar invite (useful for
            creating many unique one time use invites).
            |default| :data:`False`
        target_type: Optional[:class:`~.pincer.objects.guild.invite.InviteTargetType`]
            The type of target for the invite.
            |default| :data:`None`
        target_user_id: Optional[:class:`~.pincer.utils.Snowflake`]
            The id of the user whose stream to display for this invite. Required
            if ``target_type`` is ``STREAM``, the user must be streaming in the
            channel.
            |default| :data:`None`
        target_application_id: Optional[:class:`~.pincer.utils.Snowflake`]
            The id of the embedded application to open for this invite. Required
            if ``target_type`` is ``EMBEDDED_APPLICATION``, the application must
            have the ``EMBEDDED`` flag.
            |default| :data:`None`
        reason: Optional[:class:`str`]
            The reason of the invite creation.
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.invite.Invite`
            The invite object.
        """
        return Invite.from_dict(
            await self._http.post(
                f"channels/{self.id}/invites",
                headers={"X-Audit-Log-Reason": reason},
                data={
                    "max_age": max_age,
                    "max_uses": max_uses,
                    "temporary": temporary,
                    "unique": unique,
                    "target_type": target_type,
                    "target_user_id": target_user_id,
                    "target_application_id": target_application_id,
                },
            )
        )

    async def list_active_threads(self) -> ThreadsResponse:
        """|coro|
        Returns all active threads in the channel, including public and
        private threads. Threads are ordered by their id, in descending order.

        Returns
        -------
        :class:`~pincer.objects.channel.ThreadsResponse`
            The response object.
        """
        return ThreadsResponse.from_dict(
            self._http.get(f"channels/{self.id}/threads/active")
        )

    async def list_public_archived_threads(
        self, before: Optional[Timestamp] = None, limit: Optional[int] = None
    ) -> ThreadsResponse:
        """|coro|
        Returns archived threads in the channel that are public.
        When called on a ``GUILD_TEXT`` channel, returns threads of type
        ``GUILD_PUBLIC_THREAD``. When called on a ``GUILD_NEWS`` channel returns
        threads of type ``GUILD_NEWS_THREAD``. Threads are ordered by
        ``archive_timestamp``, in descending order. Requires the
        ``READ_MESSAGE_HISTORY`` permission.

        Parameters
        ----------
        before: Optional[:class:`~pincer.objects.timestamp.Timestamp`]
            Returns threads before this timestamp.
            |default| :data:`None`
        limit: Optional[:class:`int`]
            The maximum number of threads to return.
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.channel.ThreadsResponse`
            The response object.
        """
        return ThreadsResponse.from_dict(
            await self._http.get(
                f"channels/{self.id}/threads/archived/public",
                params={"before": before, "limit": limit},
            )
        )

    async def list_private_archived_threads(
        self, before: Optional[Timestamp] = None, limit: Optional[int] = None
    ) -> ThreadsResponse:
        """|coro|
        Returns archived threads in the channel that are of type
        ``GUILD_PRIVATE_THREAD``. Threads are ordered by ``archive_timestamp``,
        in descending order. Requires both the ``READ_MESSAGE_HISTORY`` and
        ``MANAGE_THREADS`` permissions.

        Parameters
        ----------
        before: Optional[:class:`~pincer.objects.timestamp.Timestamp`]
            Returns threads before this timestamp.
            |default| :data:`None`
        limit: Optional[:class:`int`]
            The maximum number of threads to return.
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.channel.ThreadsResponse`
            The response object.
        """
        return ThreadsResponse.from_dict(
            await self._http.get(
                f"channels/{self.id}/threads/archived/private",
                params={"before": before, "limit": limit},
            )
        )

    async def list_joined_private_archived_threads(
        self, before: Optional[Timestamp] = None, limit: Optional[int] = None
    ) -> ThreadsResponse:
        """|coro|
        Returns archived threads in the channel that are of type
        ``GUILD_PRIVATE_THREAD``, and the user has joined. Threads are ordered
        by their id, in descending order. Requires the ``READ_MESSAGE_HISTORY``
        permission.

        Parameters
        ----------
        before: Optional[:class:`~pincer.objects.timestamp.Timestamp`]
            Returns threads before this timestamp.
            |default| :data:`None`
        limit: Optional[:class:`int`]
            The maximum number of threads to return.
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.channel.ThreadsResponse`
            The response object.
        """

        return ThreadsResponse.from_dict(
            self._http.get(
                f"channels/{self.id}/users/@me/threads/archived/private",
                params={"before": before, "limit": limit},
            )
        )

    def __str__(self):
        """return the discord tag when object gets used as a string."""
        return self.name or str(self.id)


class TextChannel(Channel):
    """A subclass of ``Channel`` for text channels with all the same attributes."""

    @overload
    async def edit(
        self,
        name: str = None,
        type: ChannelType = None,
        position: int = None,
        topic: str = None,
        nsfw: bool = None,
        rate_limit_per_user: int = None,
        permissions_overwrites: List[Overwrite] = None,
        parent_id: Snowflake = None,
        default_auto_archive_duration: int = None,
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        """|coro|
        Edit a text channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)

    async def fetch_message(self, message_id: int) -> UserMessage:
        """|coro|
        Returns a UserMessage from this channel with the given id.

        Parameters
        ----------
        message_id : :class: int
            The message ID to look for.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The requested message.
        """
        return UserMessage.from_dict(
            await self._http.get(f"channels/{self.id}/messages/{message_id}")
        )

    async def history(
        self,
        limit: int = 50,
        before: Optional[Union[int, Snowflake]] = None,
        after: Optional[Union[int, Snowflake]] = None,
        around: Optional[Union[int, Snowflake]] = None,
    ) -> AsyncIterator[UserMessage]:
        """|coro|
        Returns a list of messages in this channel.

        Parameters
        ----------
        around : Optional[Union[:class:`int`, :class:`Snowflake`]]
            The message ID to look around.
        after : Optional[Union[:class:`int`, :class:`Snowflake`]]
            The message ID to look after.
        before : Optional[Union[:class:`int`, :class:`Snowflake`]]
            The message ID to look before.
        limit : Optional[Union[:class:`int`, :class:`Snowflake`]]
            The maximum number of messages to return.

        Returns
        -------
        AsyncIterator[:class:`~pincer.objects.message.user_message.UserMessage`]
            An iterator of messages.
        """

        if limit is None:
            limit = float("inf")

        while limit > 0:
            retrieve = min(limit, 100)

            raw_messages = await self._http.get(
                f"/channels/{self.id}/messages",
                params={
                    "limit": retrieve,
                    "before": before,
                    "after": after,
                    "around": around,
                },
            )

            if not raw_messages:
                break

            for _message in raw_messages:
                yield UserMessage.from_dict(_message)

            before = raw_messages[-1]["id"]
            limit -= retrieve


class VoiceChannel(Channel):
    """A subclass of ``Channel`` for voice channels with all the same attributes."""

    @overload
    async def edit(
        self,
        name: str = None,
        position: int = None,
        bitrate: int = None,
        user_limit: int = None,
        permissions_overwrites: List[Overwrite] = None,
        rtc_region: str = None,
        video_quality_mod: int = None,
    ) -> VoiceChannel:
        ...

    async def edit(self, **kwargs):
        """|coro|
        Edit a voice channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)


class GroupDMChannel(Channel):
    """A subclass of ``Channel`` for Group DMs"""


class CategoryChannel(Channel):
    """A subclass of ``Channel`` for categories channels
    with all the same attributes.
    """


class NewsChannel(Channel):
    """A subclass of ``Channel`` for news channels with all the same attributes."""

    @overload
    async def edit(
        self,
        name: str = None,
        type: ChannelType = None,
        position: int = None,
        topic: str = None,
        nsfw: bool = None,
        permissions_overwrites: List[Overwrite] = None,
        parent_id: Snowflake = None,
        default_auto_archive_duration: int = None,
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        """|coro|
        Edit a news channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)


class Thread(Channel):
    """A subclass of ``Channel`` for threads with all the same attributes."""

    async def start(
        self,
        name: Optional[str] = None,
        auto_archive_duration: Optional[int] = None,
        type_: Optional[ChannelType] = None,
        invitable: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """|coro|
        Creates a new thread that is not connected to an existing message.
        The created thread defaults to a ``GUILD_PRIVATE_THREAD``*.
        Returns a Channel on success.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The name of the thread. 1-100 characters.
            |default| :data:`None`
        auto_archive_duration**: Optional[:class:`int`]
            The duration in minutes to automatically archive the thread after
            recent activity, can be set to: ``60``, ``1440``, ``4320``, ``10080``.
            |default| :data:`None`
        type_: Optional[:class:`~pincer.objects.channel.ChannelType`]
            The type of thread to create.
            |default| :data:`None`
        invitable: Optional[:class:`bool`]
            Whether non-moderators can add other non-moderators to a thread;
            only available when creating a private thread.
            |default| :data:`None`
        rate_limit_per_user: Optional[:class:`int`]
            Amount of seconds a user has to wait before sending another message.
            (0-21600)
            |default| :data:`None`
        reason: Optional[:class:`str`]
            The reason of the thread creation.
            |default| :data:`None`

        \\*: Creating a private thread requires the server to be boosted.
        The guild features will indicate if that is possible for the guild.

        \\*\\*: The 3 day and 7 day archive durations require the server to be boosted.
        The guild features will indicate if that is possible for the guild.

        Returns
        -------
        :class:`~pincer.objects.channel.Channel`
            The created thread.
        """
        return Channel.from_dict(
            await self._http.post(
                f"channels/{self.id}/threads",
                headers={"X-Audit-Log-Reason": reason},
                data={
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "type": type_,
                    "invitable": invitable,
                    "rate_limit_per_user": rate_limit_per_user,
                },
            ),
        )

    async def start_with_message(
        self,
        message: Optional[UserMessage],
        name: Optional[str] = None,
        auto_archive_duration: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """|coro|
        Creates a new thread from an existing message. Returns a Channel on
        success.

        When called on a ``GUILD_TEXT`` channel, creates a ``GUILD_PUBLIC_THREAD``.
        When called on a ``GUILD_NEWS`` channel, creates a ``GUILD_NEWS_THREAD``.

        The id of the created thread will be the same as the id of the message,
        and as such a message can only have a single thread created from it.

        Parameters
        ----------
        message: :class:`~pincer.objects.message.user_message.UserMessage`
            The message to create the thread from.
            |default| data:`None`
        name: Optional[:class:`str`]
            The name of the thread. 1-100 characters.
            |default| data:`None`
        auto_archive_duration: Optional[:class:`int`]
            The duration in minutes to automatically archive the thread after
            recent activity, can be set to: ``60``, ``1440``, ``4320``, ``10080``.
            |default| data:`None`
        rate_limit_per_user: Optional[:class:`int`]
            Amount of seconds a user has to wait before sending another message.
            (0-21600)
            |default| data:`None`
        reason: Optional[:class:`str`]
            The reason of the thread creation.
            |default| data:`None`

        The 3 day and 7 day archive durations require the server to be boosted.
        The guild features will indicate if a server is able to use those settings.

        Returns
        -------
        :class:`~pincer.objects.channel.Channel`
            The created thread.
        """
        return Channel.from_dict(
            await self._http.post(
                f"channels/{self.id}/messages/{message.id}/threads",
                headers={"X-Audit-Log-Reason": reason},
                data={
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "rate_limit_per_user": rate_limit_per_user,
                },
            )
        )

    async def join(self):
        """|coro|
        Adds the current user to a thread.
        Also requires the thread to not be archived.
        """
        await self._http.put(f"channels/{self.id}/thread-members/@me")

    async def add_member(self, user: User):
        """|coro|
        Adds another member to a thread.
        Requires the ability to send messages in the thread.
        Also requires the thread to not be archived.

        Parameters
        ----------
        user: :class:`~pincer.objects.user.User`
            The user to add to the thread.
        """
        await self._http.put(f"channels/{self.id}/thread-members/{user.id}")

    async def leave(self):
        """|coro|
        Removes the current user from a thread.
        Also requires the thread to not be archived.
        """
        await self._http.delete(f"channels/{self.id}/thread-members/@me")

    async def remove_member(self, user: User):
        """|coro|
        Removes another member from a thread. Requires the ``MANAGE_THREADS``
        permission, or the creator of the thread if it is a
        ``GUILD_PRIVATE_THREAD``. Also requires the thread to not be archived.

        Parameters
        ----------
        user: :class:`~pincer.objects.user.User`
            The user to remove from the thread.
        """
        await self._http.delete(f"channels/{self.id}/thread-members/{user.id}")

    async def get_member(self, user: User) -> ThreadMember:
        """|coro|
        Returns a thread member object for the specified user if they are a
        member of the thread.

        Parameters
        ----------
        user: :class:`~pincer.objects.user.User`
            The user to get the thread member for.

        Returns
        -------
        :class:`~pincer.objects.channel.ThreadMember`
            The thread member object.
        """
        return ThreadMember.from_dict(
            await self._http.get(f"channels/{self.id}/thread-members/{user.id}")
        )

    def list_members(self) -> APIDataGen[ThreadMember]:
        """|coro|
        Fetches all the thread members for the thread. Returns an iterator of
        ThreadMember objects.

        Returns
        -------
        AsyncIterator[:class:`~pincer.objects.channel.ThreadMember`]
            An iterator of thread members.
        """
        return APIDataGen(
            ThreadMember, self._http.get(f"channels/{self.id}/thread-members")
        )


class PublicThread(Thread):
    """A subclass of ``Thread`` for public threads with all the same attributes."""


class PrivateThread(Thread):
    """A subclass of ``Thread`` for private threads with all the same attributes."""


@dataclass(repr=False)
class ThreadsResponse(APIObject):
    """A class representing a response from the API for a list of threads."""

    threads: AsyncIterator[Thread]
    members: AsyncIterator[ThreadMember]
    has_more: bool


@dataclass(repr=False)
class ChannelMention(APIObject):
    """Represents a Discord Channel Mention object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the channel
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild containing the channel
    type: :class:`~pincer.objects.guild.channel.ChannelType`
        The type of channel
    name: :class:`str`
        The name of the channel
    """

    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


# noinspection PyTypeChecker
_channel_type_map: Dict[ChannelType, Channel] = {
    ChannelType.GUILD_TEXT: TextChannel,
    ChannelType.GUILD_VOICE: VoiceChannel,
    ChannelType.GROUP_DM: GroupDMChannel,
    ChannelType.GUILD_CATEGORY: CategoryChannel,
    ChannelType.GUILD_NEWS: NewsChannel,
    ChannelType.GUILD_PUBLIC_THREAD: PublicThread,
    ChannelType.GUILD_PRIVATE_THREAD: PrivateThread,
}
