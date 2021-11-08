Quickstart
==========

Before starting make sure Pincer is installed. See :doc:`installing`.


Basic on_ready bot
------------------

For a basic bot, creating a :class:`~.Client` class works well. 

.. code-block:: python

	from time import perf_counter
	from pincer import Client

	client = Client("TOKEN")

	@client.event
	async def on_ready():
		print(f"Logged in as {client.bot} after {perf_counter()} seconds.")

	client.run()


Inheriting from Client
----------------------

Inheriting from :class:`~.Client` allows more flexibility and enables advance usage for a bot.

.. code-block:: python

	from time import perf_counter
	from pincer import Client

	class Bot(Client):
		def __init__(self, token):
			super(Bot, self).__init__(token)

		@Client.event
		async def on_ready(self):
			print(f"Logged in as {self.bot} after {perf_counter()} seconds.")

	bot = Bot("TOKEN")
	bot.run()


Implementing Slash Commands
---------------------------

Using slash commands is as easy as adding the :func:`~pincer.commands.command` decorator on a function and using Python annotations to specify the argument types.
Available types are as follows:

- str - String
- int - Integer
- bool - Boolean
- float - Number
- pincer.objects.User - User
- pincer.objects.Channel - Channel
- pincer.objects.Role - Role
- Mentionable is not implemented

.. code-block:: python

	from pincer import Client, command

	class Bot(Client):
		...
		@command(description="Add two numbers!")
		async def add(self, first: int, second: int):
			return f"The addition of `{first}` and `{second}` is `{first + second}`"


Sending private messages
------------------------

See :class:`~.Message` for more.

.. code-block:: python

	from pincer import Client, command, Message

	class Bot(Client):
		...
		@command(description="Sends a DM to the user.")
		async def private_say(self, message: str):
			return Message(message, flags=InteractionFlags.EPHEMERAL)


Sending Embeds
--------------

See :class:`~.Embed` for more

.. code-block:: python

	from pincer import Client, command, Embed

	class Bot(Client):
		...
		@command(description="Pincer Informational Embed")
		async def an_embed(self, message: str):
			return Embed(
				title="Pincer",
				description=(
					"🚀 An asynchronous python API wrapper meant to replace"
					" discord.py\n> Snappy discord api wrapper written "
					"with aiohttp & websockets"
				)
			).add_field(
				name="**Github Repository**",
				value="> https://github.com/Pincer-org/Pincer"
			).set_thumbnail(
				url="https://pincer.dev/img/icon.png"
			).set_image(
				url=(
					"https://repository-images.githubusercontent.com"
					"/400871418/045ebf39-7c6e-4c3a-b744-0c3122374203"
				)
			)
