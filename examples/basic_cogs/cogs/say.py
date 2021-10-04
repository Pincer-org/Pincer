from pincer import command, Client
from pincer.objects import Embed, MessageContext


class SayCog:
    @command(description="Say something as the bot!")
    async def say(self: Client, ctx: MessageContext, message: str):
        return Embed("", f"{ctx.author.user.mention} said:\n{message}")


setup = SayCog
