Interactions
============

Pincer makes it extremely easy to create an interaction. All you need to do is create a method with the `@command` decorator.

.. note::
    Although purely functional bots are possible, it's recommended to inherit from the `Client` class as seen in the example below.

.. code-block:: python

  from pincer import Client
  from pincer.commands import command

  class Bot(Client):
    @command
    async def some_command(self):
      ...

  bot = Bot("TOKEN")
  bot.run()

This registers a command called "some_command". It's pretty useless right now, so let's take a closer look at what else you can do.

.. note::
    If you're not seeing your command register, it's likely because it takes up to one hour for a global slash command to do so.
    Specify the guild in the command decorator to have application commands register instantly.

To register your command to a guild do:

.. code-block:: python

    @command(guild=MY_GUILD_ID)
    async def some_command(self):
        ...

Sending messages to the user is extremely easy. What you want to return is inferred by the object's return type. A :class:`str` can be returned to send a text message.
Here's a simple ping command.

.. code-block:: python

    @command
    async def ping(self):
        return "pong"


If you need access to more information, you can pass in the :class:`ctx <~pincer.objects.message.context.MessageContext>` object.

.. note::
    ``ctx`` and ``self`` should be those exact names or the correct value will not be passed in.

.. code-block:: python

    from pincer.objects import MessageContext
    ...

    @command
    async def hello(self, ctx: MessageContext):
        # Returns the name of the user that initiated the interaction
        return f"hello {ctx.author}"

Application Command Types
-------------------------
Pincer provides an API for all three interaction command types. The only thing that varies is the function signature.

.. code-block:: python

    from pincer.commands import command, user_command, message_command
    from pincer.objects import MessageContext, UserMessage, User
    ...

    @command
    # Can have any amount of inputs
    async def ping(self, ctx: MessageContext, arg1: str, arg2: str):
        return "pong"

    # Must have a parameter for users. User can be a GuildMember. All User
    # methods are available to GuildMember because GuildMember inherits from
    # User.
    @user_command
    async def user_ping(self, ctx: MessageContext, user: User):
        return "pong"

    # Must have a parameter for messages.
    @message_command
    async def message_ping(self, ctx: MessageContext, message: UserMessage):
        return "pong"

Interaction Timeout
-------------------
Interactions time out after 3 seconds. To extend the timeout to 15 minutes you can run :meth:`ack` from
:class:`~pincer.objects.MessageContext`. :class:`~pincer.objects.app.interaction_flags.InteractionFlags` is available in this method.

Arguments
---------

Every parameter besides ``ctx`` and ``self`` is inferred to be a slash command argument.
Notice how `word` is typehinted as string. Pincer uses type hints to infer the argument type that you want.

.. code-block:: python

    @command
    async def say(self, word: str):
        return word

The list of possible type hints is as follows:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Class
     - Command Argument Type
   * - :class:`str`
     - String
   * - :class:`int`
     - Integer
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

You might want to specify more information for your arguments. If you want a description for your command, you will have to use the
:class:`~pincer.commands.arg_types.Description` type. Modifier types like this need to be inside of the :class:`~pincer.commands.arg_types.CommandArg`
type.

.. code-block:: python

    from pincer.commands import CommandArg, Description
    from pincer.objects import MessageContext

    @command
    async def say(
        self,
        ctx: MessageContext,
        word: CommandArg[
          str,
          # This will likely be marked as incorrect by your linter but it is
          # valid Python. Simply append # type: ignore for most linters and
          # noqa: F722 if you are using Flake8.
          Description["A word that the bot will say."]  # type: ignore # noqa: F722
        ]
    ):
        # Returns the name of the user that initiated the interaction
        return word

Parameters will be an optional slash command arguments if they have a default value in Python.

.. code-block:: python

    @command
    async def say(
        self,
        word: str = "apple"  # Word is not optional
    ):
        return word

These are the available modifiers:

.. list-table::
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
     - The maximum value for a number.
     - :class:`int`, :class:`float`
   * - :class:`~pincer.objects.arg_types.MinValue`
     - The minimum value for a number.
     - :class:`int`, :class:`float`

Return Types
------------
:class:`str` isn't the only thing you can return. For a more complex message, you can return a :class:`~pincer.objects.message.message.Message` object.
The message object allows you to return embeds and attachments. :class:`~pincer.objects.app.interaction_flags.InteractionFlags` are only available in the response
if you return a :class:`~pincer.objects.message.message.Message` object.

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
            " discord.py\n> Snappy discord api wrapper written"
            " with aiohttp & websockets"
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
        " discord.py\n> Snappy discord api wrapper written"
        " with aiohttp & websockets"
      )
    )

.. list-table:: Possible Return Types
   :widths: 50 50
   :header-rows: 1

   * - Return Type
     - Discord Message
   * - :class:`str`
     - text only message
   * - :class:`~pincer.objects.message.embed.Embed`
     - Discord embed
   * - :class:`~pincer.objects.message.file.File`
     - file attachment
   * - :class:`PIL.Image.Image`
     - single image attachment


Sending Messages Without Return
-------------------------------
The :class:`~pincer.objects.message.context.MessageContext` object provides methods to send a response to an interaction.

.. code-block:: python

    from pincer.objects import MessageContext, Message

    @command
    async def some_command(self, ctx: MessageContext):
        await ctx.send("Hello world!") # Sends hello world as the response to the interaction
        return # No response will be sent now that the interaction has been completed

    @command
    async def some_other_command(self, ctx: MessageContext):
        await ctx.channel.send("Hello world!") # Sends a message in the channel
        return "Hello world 2" # This is sent because the interaction was not "used up"
