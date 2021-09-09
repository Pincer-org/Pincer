from pincer import command
from pincer.client import Client


@Client.event
async def on_ready(self):
    print(f"Started client on {self.bot}\n"
          "Registered commands: " + ", ".join(self.chat_commands))


@command(description="Say something as the bot!")
async def say(message: str):
    return message


@command(description="Add two numbers!")
async def add(first: int, second: int):
    return f"The addition of `{first}` and `{second}` is `{first + second}`"


if __name__ == "__main__":
    Client("XXXYOURBOTTOKENHEREXXX").run()
