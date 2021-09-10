Quickstart
==========

Before starting make sure Pincer is installed. See :doc:`installing`.


Basic on_ready bot
------------------

For a basic bot, creating a :class:`~.client.Client` class works well. 

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

Inheriting from :class:`~.client.Client` allows more flexibility and enables advance usage for a bot.

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


