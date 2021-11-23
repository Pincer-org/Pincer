from pincer import Client
from pincer.commands import command, CommandArg, Description
from pincer.objects import Message, InteractionFlags, Embed


@Client.event
async def on_ready(self):
    print(
        f"Started client on {self.bot}\n"
        "Registered commands: " + ", ".join(self.chat_commands)
    )


@command(description="Say something as the bot!")
async def say(
    message: CommandArg[str, Description["The content of the message"]]
):
    return message


@command(description="Add two numbers!")
async def add(
    first: CommandArg[int, Description["The first number"]],
    second: CommandArg[int, Description["The second number"]],
):
    return f"The addition of `{first}` and `{second}` is `{first + second}`"


@command(guild=1324567890)
async def private_say(
    message: CommandArg[str, Description["The content of the message"]]
):
    return Message(message, flags=InteractionFlags.EPHEMERAL)


@command(description="How to make embed!")
async def pincer_embed():
    return (
        Embed(
            title="Pincer - 0.6.4",
            description=(
                "🚀 An asynchronous python API wrapper meant to replace"
                " discord.py\n> Snappy discord api wrapper written "
                "with aiohttp & websockets"
            ),
        )
        .add_field(
            name="**Github Repository**",
            value="> https://github.com/Pincer-org/Pincer",
        )
        .set_thumbnail(url="https://pincer.dev/img/icon.png")
        .set_image(
            url=(
                "https://repository-images.githubusercontent.com"
                "/400871418/045ebf39-7c6e-4c3a-b744-0c3122374203"
            )
        )
    )


if __name__ == "__main__":
    Client("XXXYOURBOTTOKENHEREXXX").run()
