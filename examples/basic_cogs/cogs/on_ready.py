from pincer import Client


class OnReadyCog:
    @Client.event
    async def on_ready(self: Client):
        print(f"Started client on {self.bot}\n"
              "Registered commands: " + ", ".join(self.chat_commands))


setup = OnReadyCog
