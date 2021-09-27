from random import randint
from typing import Tuple

import aiohttp

from pincer import Client, command
from pincer.exceptions import CommandCooldownError
from pincer.objects import Embed, MessageContext, Message, InteractionFlags


class Bot(Client):
    MEME_URL = "https://some-random-api.ml/meme"

    @staticmethod
    def random_color():
        return int(hex(randint(0, 16581375)), 0)

    async def get_meme(self) -> Tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.MEME_URL) as response:
                data = await response.json()

                caption = data.get("caption", "Oops, something went wrong!")
                image = data.get("image")
                return caption, image

    @Client.event
    async def on_ready(self):
        print("Successfully created discord client on", self.bot)

    @command(
        cooldown=1,
        cooldown_scale=3
    )
    async def meme(self):
        caption, image = await self.get_meme()

        return Embed(caption, color=self.random_color()) \
            .set_image(image) \
            .set_footer("Provided by some-random-api.ml",
                        "https://i.some-random-api.ml/logo.png")

    @Client.event
    async def on_command_error(self, ctx: MessageContext, error: Exception):
        if isinstance(error, CommandCooldownError):
            return Message(
                embeds=[
                    Embed(
                        "Oops...",
                        f"The `{ctx.command.app.name}` command can only be used"
                        f" `{ctx.command.cooldown}` time*(s)* every "
                        f"`{ctx.command.cooldown_scale}` second*(s)*!",
                        self.random_color()
                    )
                ],
                flags=InteractionFlags.EPHEMERAL
            )
        raise error


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
