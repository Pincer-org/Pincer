from pincer import Client
from pincer.objects import MessageContext, Embed


class ErrorHandler:
    @Client.event
    async def on_command_error(self, ctx: MessageContext, error: Exception):
        return Embed(
            "Oops...",
            "An error occurred while trying to execute the "
            f"`{ctx.command.app.name}` command! Please retry later!",
            color=0xFF0000,
        ).add_field("Exception:", f"```\n{type(error).__name__}:\n{error}\n```")


setup = ErrorHandler
