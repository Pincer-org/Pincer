from pincer import Client, command
from pincer.objects import Message, InteractionFlags


class Bot(Client):
    @Client.event
    async def on_ready(self):
        print(f"Started client on {self.bot}\n"
              "Registered commands: " + ", ".join(self.chat_commands))

    @command(description="Say something as the bot!")
    async def say(self, message: str):
        return message

    @command(description="Add two numbers!")
    async def add(self, first: int, second: int):
        return f"The addition of `{first}` and `{second}` is `{first + second}`"

    @command(guild=1324567890)
    async def private_say(self, message: str):
        return Message(message, flags=InteractionFlags.EPHEMERAL)


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
