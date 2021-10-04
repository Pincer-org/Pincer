from pincer import command
from pincer.objects import Embed, MessageContext


class SayCog:
    @command(description="Say something as the bot!")
    async def say(self, ctx: MessageContext, message: str):
        return Embed("", f"{ctx.author.user.mention} said:\n{message}")


setup = SayCog
