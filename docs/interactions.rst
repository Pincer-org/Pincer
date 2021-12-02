Interactions
============

Pincer makes it extemely easy to create an interaction. All you need to do is create a method with the `@command` decorator.

.. note::
    Although purely functional bots are possible, its reccomended to inherit from the `Client` class as seen in the example below.

.. code-block:: python

  from pincer import Client
  from pincer.commands import command

  class Bot(Client):
    @command
    async def some_command(self):
      pass

  bot = Bot("TOKEN")
  bot.run()

This registers a command called "some_command". Its pretty useless right now so lets take a closer look at what else you can do.

.. note::
    If you aren't seing your command register, its likely because it takes up to one hour for a global slash command.
    Specify the guild in the command decorator to have application commands register instantly.

To register your command a guild do:

.. code-block:: python

    @command(guild=SOME_NUMBER)
    async def some_command(self):
        pass

Sending messages to the user is extemely easy. What you want to return is inferred by the object's return type. A :class:`str` can be returned to send an image.
Heres a simple ping command.

.. code-block:: python

    @command
    async def ping(self):
        return "pong"


If you need access to more information, you can pass in the :data:`ctx` object.

.. note::
    `ctx` and `self` should be those exact names or the correct value will not be passed in.

.. code-block:: python

    from pincer.objects import MessageContext
    ...

    @command
    async def hello(self, ctx: MessageContext):
        # Returns the name of the user that initiated the interaction
        return f"hello {ctx.author}"

Interaction Timeout
-------------------
Interactions time out after 3 seconds. To extend the timeout to 15 minutes you can run :meth:`ack` from
:class:`~pincer.objects.MessageContext`.

Arguments
---------

Arguments are more variables in the command. Notice how `word` is typehinted as string.
Pincer uses type hints to infer the argument type that you want.

.. code-block:: python

    @command
    async def say(self, word: str):
        return word

The list of possible type hints is as follows:

.. list-table:: Title
   :widths: 50 50
   :header-rows: 1

   * - Class
     - Command Argument Type
   * - :class:`str`
     - String
   * - :class:`int`
     - Interger
   * - :class:`bool`
     - Boolean
   * - :class:`float`
     - Number
   * - :class:`pincer.objects.User`
     - User
   * - :class:`pincer.objects.Channel`
     - Channel
   * - :class:`pincer.objects.Role`
     - Role
   * - :class:`pincer.objects.Mentionable`
     - Mentionable

You might want to specify more information for your arguments. If you want a description for your command you will have to use the
:class:`~pincer.commands.arg_types.Description` type. Modifier types like this need to be inside of the :class:`~pincer.commands.arg_types.CommandArg`
type.

.. code-block:: python

    from pincer.commands import CommandArg, Description
    from pincer.objects import MessageContext

    @command
    async def say(self,
        ctx: MessageContext,
        word: CommandArg[
          str,
          # This will likely marked as incorrect by your linter but it is
          # valid python
          Description["A word that the bot will say."]
        ]
    ):
        # Returns the name of the user that initiated the interaction
        return word

Arguments will be an optional argument in Discord if they are an optional argument in Python.

These are the available modifiers:

.. list-table:: Modifier Types
   :widths: 25 40 35
   :header-rows: 1

   * - Modifier
     - What it does
     - Locked to types
   * - :class:`~pincer.objects.arg_types.Description`
     - Description of a command option.
     -
   * - :class:`~pincer.objects.arg_types.Choices`
     - Application command choices.
     - :class:`str`, :class:`int`, :class:`float`
   * - :class:`~pincer.objects.arg_types.ChannelTypes`
     - A group of channel types that a user can pick from.
     - :class:`~pincer.objects.guild.channel.Channel`
   * - :class:`~pincer.objects.arg_types.MaxValue`
     - The max value for a number.
     - :class:`int`, :class:`float`
   * - :class:`~pincer.objects.arg_types.MinValue`
     - The minimum value for a number.
     - :class:`int`, :class:`float`

Return Types
------------
:class:`str` isn't the only thing you can return. For a more complex message you can return a :class:`~pincer.objects.message.message.Message` object.
The message object allows you to return embeds and attachments.

.. code-block:: python

  from pincer import Client, command, Embed
  from pincer.objects import Message, File
  ...

  @command
  async def a_complex_message(self):
    return Message(
      "This is the message's content"
      embeds=[
        Embed(
          title="Pincer",
          description=(
            "🚀 An asynchronous python API wrapper meant to replace"
            " discord.py\n> Snappy discord api wrapper written "
            "with aiohttp & websockets"
          ).set_image(
            url="attachments://some_image.png"
          )
        )
      ],
      attachments=[
        File.from_file("path/to/a/file.png", filename="new_name.png"),
        "path/to/another/file.png" # A string is inferred to be a filepath here!
      ]
    )

Attachments can also be Pillow images if Pillow is installed.

.. code-block:: python

  from PIL import Image
  ...

  attachments=[
    Image.new("RGBA", (500, 500), (255, 0, 0)), # Will automatically be named `image0.png`
    Image.new("RGB", (500, 500)), # Will automatically be named `image1.png`
    File.from_pillow_image(some_pillow_image, "this_is_the_image_name.png") # You can also do this to specify the name
  ]

Additionally, Pillow Images, Files, and Embeds can be returned directly without wrapping them in a :class:`~pincer.objects.message.message.Message` object.

.. code-block:: python

  ...
  @command
  async def a_complex_message(self):
    return Embed(
      title="Pincer",
      description=(
        "🚀 An asynchronous python API wrapper meant to replace"
        " discord.py\n> Snappy discord api wrapper written "
        "with aiohttp & websockets"
      )
    )