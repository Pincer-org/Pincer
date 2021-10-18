from random import randint
from typing import Tuple

from aiohttp import ClientSession

from pincer import Client, command
from pincer.exceptions import CommandCooldownError
from pincer.objects import Embed, MessageContext, Message, InteractionFlags
from pincer.utils import MISSING


# Create our base bot client, if you want to you can use an init an
# super call it. But that isn't required for this example.


class Bot(Client):
    # Our url from where we'll get our juicy memes!
    MEME_URL = "https://some-random-api.ml/meme"

    @staticmethod
    def random_color():
        """
        Generate a valid random Discord color!
        """
        return int(hex(randint(0, 16581375)), 0)

    async def get_meme(self) -> Tuple[str, str]:
        """
        Get a random meme from our configured MEME_URL!
        """
        # Standard aiohttp session setup:
        async with ClientSession() as session:
            # Send our HTTP get request!
            async with session.get(self.MEME_URL) as response:
                # To extract the data we need to have the json as a dict!
                data = await response.json()

                # If the json was malformed, make sure we have backup values!
                caption = data.get("caption", "Oops, something went wrong!")
                image = data.get("image", MISSING)

                # Return it as a tuple so we can easily extract the two
                # values in our method which called this!
                return caption, image

    @Client.event
    async def on_ready(self):
        # Our client has successfully started, lets let ourself know that!
        print("Successfully created discord client on", self.bot)

    @command(
        # We don't want to send too many requests to our `MEME_URL` so
        # lets use cooldowns!

        # Only allow one request
        cooldown=1,
        # For every three seconds
        cooldown_scale=3,

        # And just to make things more clear for our user on what this
        # command does, lets define a description!
        description="Get a random meme!"
    )
    async def meme(self):
        # Fetch our caption and image from our `MEME_URL`.
        caption, image = await self.get_meme()

        # Respond with an embed which contains the meme and caption!
        return Embed(caption, color=self.random_color()) \
            .set_image(image) \
            .set_footer("Provided by some-random-api.ml",
                        "https://i.some-random-api.ml/logo.png")

    @Client.event
    async def on_command_error(self, ctx: MessageContext, error: Exception):
        # OH NO, something went wrong while executing our command.
        # Don't worry tho, it might be our user whom is trespassing our
        # set cooldown. Lets check if the error is a cooldown error,
        if isinstance(error, CommandCooldownError):
            # Yeah, the user got rate limited by our cooldown.
            # Lets let them know in a private embed message!
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

        # Oh no, it wasn't a cooldown error. Lets throw it!
        raise error


if __name__ == "__main__":
    # Of course we have to run our client, you can replace the
    # XXYOURBOTTOKENHEREXX with your token, or dynamically get it
    # through a dotenv/env.
    Bot("XXXYOURBOTTOKENHEREXXX").run()
