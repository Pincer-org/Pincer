# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, overload

from ...exceptions import EmbedOverflow
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List, Optional

    from ..message.attachment import Attachment
    from ..message.component import MessageComponent
    from ..message.embed import Embed
    from ..message.user_message import UserMessage
    from ..message.user_message import AllowedMentions
    from ..user.user import User
    from ..guild.guild import Guild
    from ..guild.channel import Channel
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...client import Client


class WebhookCompatibility(Enum):
    GitHub = "github"
    Slack = "slack"
    Default = ""


class WebhookType(IntEnum):
    """Represents the type of webhook.

    Attributes
    ----------
    INCOMING:
        Incoming Webhooks can post messages to channel with a
        generated token.
    CHANNEL_FOLLOWER:
        Channel Follower Webhooks are internal webhooks used with
        Channel Following to post new messages into channels.
    APPLICATION:
        Application webhooks are webhooks used with Interactions
    """

    INCOMING = 1
    CHANNEL_FOLLOWER = 2
    APPLICATION = 3


@dataclass(repr=False)
class Webhook(APIObject):
    """Represents a Discord channel webhook.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the webhook
    type: :class:`~pincer.objects.guild.webhook.WebhookType`
        The type of the webhook
    channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The channel id this webhook is for, if any
    name: Optional[:class:`str`]
        The default name of the webhook
    avatar: Optional[:class:`str`]
        The default user avatar hash of the webhook
    application_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The bot/OAuth2 application that created this webhook
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        The user this webhook was created by
        (not returned when getting a webhook with its token)
    token: APINullable[:class:`str`]
        The secure token of the webhook
        (returned for Incoming Webhooks)
    source_guild: APINullable[:class:`~pincer.objects.guild.guild.Guild`]
        The guild of the channel that this webhook is following
        (returned for Channel Follower Webhooks)
    source_channel: APINullable[:class:`~pincer.objects.guild.channel.Channel`]
        The channel that this webhook is following
        (returned for Channel Follower Webhooks)
    url: APINullable[:class:`str`]
        The url used for executing the webhook
        (returned by the webhooks OAuth2 flow)
    guild_id: APINullable[Optional[:class:`~pincer.objects.guild.guild.Guild`]]
        The guild id this webhook is for, if any
    """

    id: Snowflake
    type: WebhookType

    channel_id: Optional[Snowflake] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    application_id: Optional[Snowflake] = None

    user: APINullable[User] = MISSING
    token: APINullable[str] = MISSING
    source_guild: APINullable[Guild] = MISSING
    source_channel: APINullable[Channel] = MISSING
    url: APINullable[str] = MISSING

    guild_id: APINullable[Optional[Snowflake]] = MISSING

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
        channel_id: Optional[Snowflake] = None,
        token: Optional[str] = None,
    ) -> Webhook:
        """
        Modifies a webhook and returns it.
        Requires the ``MANAGE_WEBHOOKS`` permission.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The new name of the webhook
        avatar: Optional[:class:`str`]
            The new avatar hash of the webhook
        channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The new channel id this webhook is for
        token: Optional[:class:`str`]
            The new token of the webhook
        """
        request_route = f"webhooks/{self.id}" + (f"/{token}" if token else "")
        request_data = {
            "name": name,
            "avatar": avatar,
            "channel_id": channel_id,
        }

        if token:
            del request_data["channel_id"]

        data = await self._http.patch(request_route, data=request_data)
        return Webhook.from_dict(data)

    async def delete(self, token: Optional[str] = None):
        """
        Deletes a webhook.
        Requires the ``MANAGE_WEBHOOKS`` permission.

        Parameters
        ----------
        token: Optional[:class:`str`]
            The token of the webhook
        """
        await self._http.delete(
            f"webhooks/{self.id}" + (f"/{token}" if token else "")
        )

    @overload
    async def execute(
        self,
        webhook_compatibility: WebhookCompatibility = WebhookCompatibility.Default,  # noqa: E501
        *,
        thread_id: Optional[Snowflake] = None,
        wait: Optional[bool] = None,
        content: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        components: Optional[List[MessageComponent]] = None,
        files: Optional[str] = None,  # TODO: Add support for files
        payload_json: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
    ):
        """|coro|
        Executes a webhook.

        Note that when sending a message, you must provide a value
        for at least one of ``content``, ``embeds``, or ``file``.

        Parameters
        ----------
        webhook_compatibility: :class:`~pincer.objects.guild.webhook.WebhookCompatibility`
            The compatibility of the webhook
        thread_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID of the thread to send message in
        wait: Optional[:class:`bool`]
            Waits for server confirmation of message send before
            response (defaults to ``true``, when ``false`` a message
            that is not saved does not return an error)
        content: Optional[:class:`str`]
            The message contents (up to 2000 characters)
        username: Optional[:class:`str`]
            Override the default username of the webhook
        avatar_url: Optional[:class:`str`]
            Override the default avatar of the webhook
        tts: Optional[:class:`bool`]
            True if this is a TTS message
        embeds: Optional[List[:class:`~pincer.objects.message.embed.Embed`]]
            Embedded ``rich`` content, up to 10 embeds
        allowed_mentions: Optional[:class:`~pincer.objects.message.user_message.AllowedMentions`]
            Allowed mentions for the message
        components: Optional[List[:class:`~pincer.objects.message.component.MessageComponent`]]
            The components to include in the message
        files: Optional[:class:`str`]
            The contents of the file being sent
        payload_json: Optional[:class:`str`]
            JSON encoded body of non-file params
        attachments: Optional[List[:class:`~pincer.objects.message.attachment.Attachment`]]
            Attachment objects with filename and description
        """
        ...

    async def execute(
        self,
        webhook_compatibility: WebhookCompatibility = WebhookCompatibility.Default,  # noqa: E501
        *,
        thread_id: Optional[Snowflake] = None,
        wait: Optional[bool] = None,
        **kwargs,
    ):
        if len(kwargs.get("embeds", [])) > 10:
            raise EmbedOverflow("You can only include up to 10 embeds")

        request_route = f"webhooks/{self.id}/{self.token}"

        # Adding the subdirectory
        if webhook_compatibility.value:
            request_route += f"/{webhook_compatibility.value}"

        # Adding query params
        if wait is not None:
            request_route += f"?{wait=}"
        if thread_id is not None:
            request_route += "&?"[wait is None] + f"{thread_id=}"

        if webhook_compatibility == WebhookCompatibility.Default:
            request_data = kwargs
        else:
            request_data = None

        await self._http.post(request_route, data=request_data)

    async def execute_github(
        self,
        *,
        thread_id: Optional[Snowflake] = None,
        wait: Optional[bool] = None,
    ):
        """|coro|
        Executes a GitHub compatible webhook.

        Parameters
        ----------
        thread_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID of the thread to send message in
        wait: Optional[:class:`bool`]
            Waits for server confirmation of message send before
            response (defaults to ``true``, when ``false`` a message
            that is not saved does not return an error)
        """
        await self.execute(
            WebhookCompatibility.GitHub, thread_id=thread_id, wait=wait
        )

    async def execute_slack(
        self,
        *,
        thread_id: Optional[Snowflake] = None,
        wait: Optional[bool] = None,
    ):
        """|coro|
        Executes a Slack compatible webhook.

        Parameters
        ----------
        thread_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID of the thread to send message in
        wait: Optional[:class:`bool`]
            Waits for server confirmation of message send before
            response (defaults to ``true``, when ``false`` a message
            that is not saved does not return an error)
        """
        await self.execute(
            WebhookCompatibility.Slack, thread_id=thread_id, wait=wait
        )

    async def get_message(
        self, message_id: Snowflake, thread_id: Snowflake
    ) -> UserMessage:
        """|coro|
        Returns a previously-sent webhook message from the same token.

        Parameters
        ----------
        message_id: :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the message to get
        thread_id: :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the thread to get the message from

        Returns
        -------
        :class:`~pincer.objects.message.message.Message`
            The message
        """
        return UserMessage.from_dict(
            await self._http.get(
                f"webhooks/{self.id}/{self.token}/messages/{message_id}",
                params={"thread_id": thread_id},
            )
        )

    async def delete_message(self, message_id: Snowflake, thread_id: Snowflake):
        """|coro|
        Deletes a message created by a webhook.

        Parameters
        ----------
        message_id: :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the message to delete
        thread_id: :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the thread to delete the message from
        """
        await self._http.delete(
            f"webhooks/{self.id}/{self.token}/messages/{message_id}"
            + (f"?{thread_id=}" if thread_id else "")
        )

    @overload
    async def edit_message(
        self,
        message_id: Snowflake,
        *,
        thread_id: Optional[Snowflake] = None,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        components: Optional[List[MessageComponent]] = None,
        files: Optional[str] = None,  # TODO: Add support for files
        payload_json: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
    ) -> UserMessage:
        """|coro|
        Edits a previously-sent webhook message from the same token.

        Parameters
        ----------
        message_id: :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the message to edit
        thread_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID of the thread the message is in
        content: Optional[:class:`str`]
            The new content of the message (up to 2000 characters)
        embeds: Optional[List[:class:`~pincer.objects.message.embed.Embed`]]
            Embedded ``rich`` content, up to 10 embeds
        allowed_mentions: Optional[:class:`~pincer.objects.message.user_message.AllowedMentions`]
            Allowed mentions for the message
        components: Optional[List[:class:`~pincer.objects.message.component.MessageComponent`]]
            The components to include in the message
        files: Optional[:class:`str`]
            The contents of the file being sent/edited
        payload_json: Optional[:class:`str`]
            JSON encoded body of non-file params
            (multipart/form-data only)
        attachments: Optional[List[:class:`~pincer.objects.message.attachment.Attachment`]]
            Attached files to keep and
            possible descriptions for new files
        """
        ...

    async def edit_message(
        self,
        message_id: Snowflake,
        *,
        thread_id: Optional[Snowflake] = None,
        **kwargs,
    ) -> UserMessage:
        if len(kwargs.get("embeds", [])) > 10:
            raise EmbedOverflow("You can only include up to 10 embeds")

        data = await self._http.patch(
            f"webhooks/{self.id}/{self.token}/messages/{message_id}"
            + (f"?{thread_id=}" if thread_id else ""),
            data=kwargs,
        )
        return UserMessage.from_dict(data)

    @classmethod
    async def from_id(
        cls, client: Client, id: Snowflake, token: Optional[str] = None
    ) -> Webhook:
        """|coro|
        Gets a webhook by its ID.

        Parameters
        ----------
        client: `~pincer.client.Client`
            The client to use to make the request.
        id: `~pincer.utils.snowflake.Snowflake`
            The ID of the webhook to get.
        token: Optional[:class:`str`]
            The token of the webhook to get.

        Returns
        -------
        `~pincer.objects.guild.webhook.Webhook`
            The webhook with the given ID.
        """
        return cls.from_dict(
            await client.http.get(
                f"webhooks/{id}" + (f"/{token}" if token else "")
            )
        )
