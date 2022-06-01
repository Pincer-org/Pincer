from typing import Any, Dict, List
from pincer import Client, Cog, command
from pincer.objects import MessageContext, Embed


class ErrorHandler(Cog):
    @Client.event
    async def on_command_error(
        self,
        ctx: MessageContext,
        error: Exception,
        args: List[Any],
        kwargs: Dict[str, Any],
    ):
        return Embed(
            "Oops...",
            "An error occurred while trying to execute the "
            f"`{ctx.interaction.data.name}` command! Please retry later!",
            color=0xFF0000,
        ).add_field("Exception:", f"```\n{type(error).__name__}:\n{error}\n```")


class OnReadyCog(Cog):
    @Client.event
    async def on_ready(self):
        print(
            f"Started client on {self.client.bot}\n"
            "Registered commands: " + ", ".join(self.client.chat_commands)
        )


class SayCog(Cog):
    @command(description="Say something as the bot!")
    async def say(self, ctx: MessageContext, message: str):
        return Embed(description=f"{ctx.author.mention} said:\n{message}")
