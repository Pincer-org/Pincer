"""
Properly welcome your new members into your server!
"""
from __future__ import annotations

import json
import logging
from asyncio import sleep
from os import getenv
from typing import TYPE_CHECKING

from aiohttp import ClientSession

from pincer import Cog, Client, command
from pincer.objects import File, Message
from pincer.objects.events.guild import GuildMemberAddEvent

if TYPE_CHECKING:
    from pincer.objects import Channel, User


class Welcome(Cog):
    channel: Channel
    BASE_API_URL = "https://api.xiler.net"
    REQUEST_HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(self, client: Client):
        super().__init__(client)
        self.__session: ClientSession = ClientSession(self.BASE_API_URL)

        with open("./cogs/templates/welcome.html") as f:
            self.template = f.read()

    def _build_html(self, user: User) -> str:
        """Build a HTML template to welcome new users!"""
        arguments = {
            "icon": user.get_avatar_url(256),
            "username": user.username,
            "discriminator": user.discriminator
        }

        res = self.template

        for key, value in arguments.items():
            res = res.replace(f"%{key}%", value)

        return res

    async def generate_welcome_for_user(self, user: User, ttl=0) -> File:
        """Generate the welcome file, this gets sent to discord!"""
        body = {
            "html": self._build_html(user),
            "config": {
                "format": "png",
                "width": 700,
                "height": 258,
                "transparent": True,
            }
        }

        async with self.__session.post(
            "/v1/html-to-image",
            # "/v1/html-to-image-chrome", # use this endpoint with the variant,
            # as it requires more modern css support
            data=json.dumps(body),
            headers=self.REQUEST_HEADERS
        ) as res:
            if res.ok:
                image_bytes = await res.read()
                return File(image_bytes, "png", f"welcome-{user.id}.png")

            logging.error(await res.read())

            # Allow a maximum of 5 retries
            if ttl < 5:
                await sleep(0.5)
                return await self.generate_welcome_for_user(user, ttl + 1)

            raise RuntimeError(
                "TTL Exceeded, not retrying request! (failed for welcomes)"
            )

    @Client.event
    async def on_ready(self):
        self.channel = await self.client.get_channel(int(getenv("WELCOME_CHANNEL")))

    @Client.event
    async def on_guild_member_add(self, event: GuildMemberAddEvent):
        banner = await self.generate_welcome_for_user(event)
        await self.channel.send(Message(attachments=[banner]))
