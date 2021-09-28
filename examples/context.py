from pincer import Client, command
from pincer.objects import Embed


class Bot(Client):

    @command(description="Say something as the bot!")
    async def say(self, ctx, content: str) -> Embed:
        # Using the ctx to get the command author
        return Embed(
            description=f"{ctx.author.user.mention} said {content}"
        )

    @Client.event
    async def on_ready(self):
        # Our client has successfully started, lets let ourself know that!
        print("Logged in as", self.bot)


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
