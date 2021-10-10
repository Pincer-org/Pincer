from pincer import Client


class OnReadyCog:
    def __init__(self, client: Client):
        self.client = client

    @Client.event
    async def on_ready(self):
        print(
            f"Started client on {self.client.bot}\n"
            "Registered commands: " + ", ".join(self.client.chat_commands)
        )


setup = OnReadyCog
