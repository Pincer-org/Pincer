# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import signal
from asyncio import (
    iscoroutinefunction,
    ensure_future,
    create_task,
    get_event_loop,
)
from collections import defaultdict
from functools import partial
from inspect import isasyncgenfunction
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Iterable,
    OrderedDict,
    Tuple,
    Union,
    overload,
    TYPE_CHECKING,
)


from .cog import CogManager
from .commands.interactable import Interactable
from .objects.app.command import InteractableStructure

from . import __package__
from .commands import ChatCommandHandler
from .core import HTTPClient
from .core.gateway import GatewayInfo, Gateway

from .exceptions import InvalidEventName, GatewayConnectionError

from .middleware import middleware
from .objects import (
    Role,
    Channel,
    DefaultThrottleHandler,
    User,
    Guild,
    Intents,
    GuildTemplate,
    StickerPack,
    UserMessage,
    Connection,
    File,
    StageInstance,
    PrivacyLevel,
)
from .objects.guild.channel import GroupDMChannel
from .utils import APIObject
from .utils.conversion import remove_none
from .utils.event_mgr import EventMgr
from .utils.extraction import get_index
from .utils.insertion import should_pass_cls, should_pass_gateway
from .utils.shards import calculate_shard_id
from .utils.types import CheckFunction
from .utils.types import Coro

if TYPE_CHECKING:
    from .utils.snowflake import Snowflake
    from .core.dispatch import GatewayDispatch
    from .objects.app.throttling import ThrottleInterface
    from .objects.guild import Webhook

    from collections.abc import AsyncIterator

_log = logging.getLogger(__package__)

MiddlewareType = Optional[Union[Coro, Tuple[str, List[Any], Dict[str, Any]]]]

_event = Union[str, InteractableStructure[None]]
_events: Dict[str, Optional[Union[List[_event], _event]]] = defaultdict(list)


def event_middleware(call: str, *, override: bool = False):
    """Middleware are methods which can be registered with this decorator.
    These methods are invoked before any ``on_`` event.
    As the ``on_`` event is the final call.

    A default call exists for all events, but some might already be in
    use by the library.

    If you know what you are doing, you can override these default
    middleware methods by passing the override parameter.

    The method to which this decorator is registered must be a coroutine,
    and it must return a tuple with the following format:

    .. code-block:: python

        tuple(
            key for next middleware or final event [str],
            args for next middleware/event which will be passed as *args
                [list(Any)],
            kwargs for next middleware/event which will be passed as
                **kwargs [dict(Any)]
        )

    Two parameters are passed to the middleware. The first parameter is
    the current socket connection with and the second one is the payload
    parameter which is of type :class:`~.core.dispatch.GatewayDispatch`.
    This contains the response from the discord API.

    :Implementation example:

    .. code-block:: python3

         @event_middleware("ready", override=True)
         async def custom_ready(_, payload: GatewayDispatch):
             return "on_ready", [
                 User.from_dict(payload.data.get("user"))
             ]

         @Client.event
         async def on_ready(bot: User):
             print(f"Signed in as {bot}")

    Parameters
    ----------
    call : :class:`str`
        The call that the function should tie to
    override : :class:`bool`
        If it should override default middleware,
        usually shouldn't be used |default| :data:`False`
    """

    def decorator(func: Coro):
        if override:
            _log.warning(
                "Middleware overriding has been enabled for `%s`."
                " This might cause unexpected behavior.",
                call,
            )

        if not override and callable(_events.get(call)):
            raise RuntimeError(
                f"Middleware event with call `{call}` has "
                "already been registered"
            )

        async def wrapper(cls, gateway: Gateway, payload: GatewayDispatch):
            _log.debug("`%s` middleware has been invoked", call)

            return await func(cls, gateway, payload)

        _events[call] = wrapper
        return wrapper

    return decorator


for event, middleware_ in middleware.items():
    event_middleware(event)(middleware_)


class Client(Interactable, CogManager):
    """The client is the main instance which is between the programmer
    and the discord API.

    This client represents your bot.

    Attributes
    ----------
    bot: :class:`~objects.user.user.User`
        The user object of the client
    received_message: :class:`str`
        The default message which will be sent when no response is given.
    http: :class:`~core.http.HTTPClient`
        The http client used to communicate with the discord API

    Parameters
    ----------
    token : :class:`str`
        The token to login with your bot from the developer portal
    received : Optional[:class:`str`]
        The default message which will be sent when no response is given.
        |default| :data:`None`
    intents : Optional[Union[Iterable[:class:`~objects.app.intents.Intents`], :class:`~objects.app.intents.Intents`]]
        The discord intents to use |default| :data:`Intents.all()`
    throttler : Optional[:class:`~objects.app.throttling.ThrottleInterface`]
        The cooldown handler for your client,
        defaults to :class:`~.objects.app.throttling.DefaultThrottleHandler`
        *(which uses the WindowSliding technique)*.
        Custom throttlers must derive from
        :class:`~pincer.objects.app.throttling.ThrottleInterface`.
        |default| :class:`~pincer.objects.app.throttling.DefaultThrottleHandler`
    """  # noqa: E501

    def __init__(
        self,
        token: str,
        *,
        received: str = None,
        intents: Intents = None,
        throttler: ThrottleInterface = DefaultThrottleHandler,
        reconnect: bool = True,
    ):
        def sigint_handler(_signal, _frame):
            _log.info("SIGINT received, shutting down...")

            # A print statement to make sure the user sees the message
            print("Closing the client loop, this can take a few seconds...")

            create_task(self.http.close())
            if self.loop.is_running():
                self.loop.stop()

        signal.signal(signal.SIGINT, sigint_handler)

        if isinstance(intents, Iterable):
            intents = sum(intents)

        if intents is None:
            intents = Intents.all()

        self.intents = intents
        self.reconnect = reconnect
        self.token = token

        self.bot: Optional[User] = None
        self.received_message = received or "Command arrived successfully!"
        self.http = HTTPClient(token)
        APIObject.bind_client(self)

        self.throttler = throttler

        async def get_gateway():
            return GatewayInfo.from_dict(await self.http.get("gateway/bot"))

        self.loop = get_event_loop()
        self.event_mgr = EventMgr(self.loop)

        self.gateway: GatewayInfo = self.loop.run_until_complete(get_gateway())
        self.shards: OrderedDict[int, Gateway] = OrderedDict()

        # The guild and channel value is only registered if the Client has the GUILDS
        # intent.
        self.guilds: Dict[Snowflake, Optional[Guild]] = {}
        self.channels: Dict[Snowflake, Optional[Channel]] = {}

        ChatCommandHandler.managers.append(self)

        super().__init__()

    @property
    def chat_commands(self) -> List[str]:
        """List[:class:`str`]: List of chat commands

        Get a list of chat command calls which have been registered in
        the :class:`~pincer.commands.ChatCommandHandler`\\.
        """
        return [
            cmd.metadata.name for cmd in ChatCommandHandler.register.values()
        ]

    @property
    def guild_ids(self) -> List[Snowflake]:
        """
        Returns a list of Guilds that the client is a part of

        Returns
        -------
        List[:class:`pincer.utils.snowflake.Snowflake`]
        """
        return self.guilds.keys()

    @staticmethod
    def event(coroutine: Coro):
        """A decorator to register a Discord gateway event listener.
        This event will get called when the client receives a new event
        update from Discord which matches the event name.

        The event name gets pulled from your method name, and this must
        start with ``on_``.
        This forces you to write clean and consistent code.

        This decorator can be used in and out of a class, and all
        event methods must be coroutines. *(async)*

        :Example usage:

        .. code-block:: python3

             # Function based
             from pincer import Client

             client = Client("token")

             @client.event
             async def on_ready():
                 print(f"Signed in as {client.bot}")

             if __name__ == "__main__":
                 client.run()

        .. code-block :: python3

             # Class based
             from pincer import Client

             class MyClient(Client):
                 @Client.event
                 async def on_ready(self):
                     print(f"Signed in as {self.bot}")

             if __name__ == "__main__":
                 MyClient("token").run()

        Raises
        ------
        TypeError
            If the function is not a coro
        InvalidEventName
            If the function name is not a valid event (on_x)
        """
        if not iscoroutinefunction(coroutine) and not isasyncgenfunction(
            coroutine
        ):
            raise TypeError(
                "Any event which is registered must be a coroutine function"
            )

        name: str = coroutine.__name__.lower()

        if not name.startswith("on_"):
            raise InvalidEventName(
                f"The event named `{name}` must start with `on_`"
            )

        if name == "on_command_error" and _events.get(name):
            raise InvalidEventName(
                f"The `{name}` event can only exist once. This is because "
                "it gets treated as a command and can have a response."
            )

        event = InteractableStructure(call=coroutine)

        _events[name].append(event)
        return event

    @staticmethod
    def get_event_coro(
        name: str,
    ) -> List[Optional[InteractableStructure[None]]]:
        """get the coroutine for an event

        Parameters
        ----------
        name : :class:`str`
            name of the event

        Returns
        -------
        List[Optional[:class:`~pincer.objects.app.command.InteractableStructure`[None]]]
        """
        calls = _events.get(name.strip().lower())

        return (
            []
            if not calls
            else [
                call
                for call in calls
                if isinstance(call, InteractableStructure)
            ]
        )

    @staticmethod
    def execute_event(
        events: List[InteractableStructure], gateway: Gateway, *args, **kwargs
    ):
        """Invokes an event.

        Parameters
        ----------
        calls: List[:class:`~pincer.objects.app.command.InteractableStructure`]
            The call (method) to which the event is registered.

        \\*args:
            The arguments for the event.

        \\*\\*kwargs:
            The named arguments for the event.
        """

        for event in events:
            call_args = args
            if should_pass_cls(event.call):
                call_args = (
                    event.manager,
                    *remove_none(args),
                )

            if should_pass_gateway(event.call):
                call_args = (call_args[0], gateway, *call_args[1:])

            ensure_future(event.call(*call_args, **kwargs))

    def run(self):
        """Start the bot."""
        ensure_future(self.start_shard(0, 1), loop=self.loop)
        self.loop.run_forever()

    def run_autosharded(self):
        """
        Runs the bot with the amount of shards specified by the Discord gateway.
        """
        num_shards = self.gateway.shards
        return self.run_shards(range(num_shards), num_shards)

    def run_shards(self, shards: Iterable, num_shards: int):
        """
        Runs shards that you specify.

        shards: Iterable
            The shards to run.
        num_shards: int
            The total amount of shards.
        """
        for shard in shards:
            ensure_future(self.start_shard(shard, num_shards), loop=self.loop)

        self.loop.run_forever()

    async def start_shard(self, shard: int, num_shards: int):
        """|coro|
        Starts a shard
        This should not be run most of the time. ``run_shards`` and ``run_autosharded``
        will likely do what you want.

        shard : int
            The number of the shard to start.
        num_shards : int
            The total number of shards.
        """

        gateway = Gateway(
            self.token,
            intents=self.intents,
            url=self.gateway.url,
            shard=shard,
            num_shards=num_shards,
        )
        await gateway.init_session()

        gateway.append_handlers(
            {
                # Gets triggered on all events
                -1: partial(self.payload_event_handler, gateway),
                # Use this event handler for opcode 0.
                0: partial(self.event_handler, gateway),
            }
        )

        self.shards[gateway.shard] = gateway
        create_task(gateway.start_loop())

    def get_shard(
        self,
        guild_id: Optional[Snowflake] = None,
        num_shards: Optional[int] = None,
    ) -> Gateway:
        """
        Returns the shard receiving events for a specified guild_id.

        ``num_shards`` is inferred from the num_shards value for the first started
        shard. If your shards do not all have the same ``num_shard`` value, you must
        specify value to get the expected result.

        Parameters
        ----------
        guild_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The guild_id of the shard to look for. If no guild id is provided, the
            shard that receives dms will be returned. |default| :data:`None`
        num_shards : Optional[:class:`int`]
            The number of shards. If no number is provided, the value will default to
            the num_shards for the first started shard. |default| :data:`None`
        """
        if not self.shards:
            raise GatewayConnectionError(
                "The client has never connected to a gateway"
            )
        if guild_id is None:
            return self.shards[0]
        if num_shards is None:
            num_shards = next(iter(self.shards.values())).num_shards
        return self.shards[calculate_shard_id(guild_id, num_shards)]

    @property
    def is_closed(self) -> bool:
        """
        Returns
        -------
        bool
            Whether the bot is closed.
        """
        return self.loop.is_running()

    def close(self):
        """
        Ensure close of the http client.
        Allow for script execution to continue.
        """
        if hasattr(self, "http"):
            create_task(self.http.close())

        self.loop.stop()

    def __del__(self):
        if self.loop.is_running():
            self.loop.stop()

        if not self.loop.is_closed():
            self.close()

    async def handle_middleware(
        self,
        payload: GatewayDispatch,
        key: str,
        gateway: Gateway,
        *args,
        **kwargs,
    ) -> Tuple[Optional[Coro], List[Any], Dict[str, Any]]:
        """|coro|

        Handles all middleware recursively. Stops when it has found an
        event name which starts with ``on_``.

        Returns a tuple where the first element is the final executor
        (so the event) its index in ``_events``.

        The second and third element are the ``*args``
        and ``**kwargs`` for the event.

        Parameters
        ----------
        payload : :class:`~pincer.core.dispatch.GatewayDispatch`
            The original payload for the event
        key : :class:`str`
            The index of the middleware in ``_events``

        Raises
        ------
        RuntimeError
            The return type must be a tuple
        RuntimeError
            Middleware has not been registered
        """
        ware: MiddlewareType = _events.get(key)
        next_call, arguments, params = ware, [], {}

        if iscoroutinefunction(ware):
            extractable = await ware(self, gateway, payload, *args, **kwargs)

            if not isinstance(extractable, tuple):
                raise RuntimeError(
                    f"Return type from `{key}` middleware must be tuple. "
                )

            next_call = get_index(extractable, 0, "")
            ret_object = get_index(extractable, 1)

        if next_call is None:
            raise RuntimeError(f"Middleware `{key}` has not been registered.")

        if next_call.startswith("on_"):
            return (next_call, ret_object)

        return await self.handle_middleware(
            payload, next_call, gateway, *arguments, **params
        )

    async def execute_error(
        self,
        error: Exception,
        gateway: Gateway,
        name: str = "on_error",
        *args,
        **kwargs,
    ):
        """|coro|

        Raises an error if no appropriate error event has been found.

        Parameters
        ----------
        error : :class:`Exception`
            The error that should be passed to the event
        name : :class:`str`
            the name of the event |default| ``on_error``

        Raises
        ------
        error
            if ``call := self.get_event_coro(name)`` is :data:`False`
        """
        if calls := self.get_event_coro(name):
            self.execute_event(calls, gateway, error, *args, **kwargs)
        else:
            raise error

    async def process_event(
        self, name: str, payload: GatewayDispatch, gateway: Gateway
    ):
        """|coro|

        Processes and invokes an event and its middleware

        Parameters
        ----------
        name : :class:`str`
            The name of the event, this is also the filename in the
            middleware directory.
        payload : :class:`~pincer.core.dispatch.GatewayDispatch`
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        try:
            key, args = await self.handle_middleware(payload, name, gateway)
            self.event_mgr.process_events(key, args)

            if calls := self.get_event_coro(key):
                self.execute_event(calls, gateway, args)

        except Exception as e:
            await self.execute_error(e, gateway)

    async def event_handler(self, gateway: Gateway, payload: GatewayDispatch):
        """|coro|

        Handles all payload events with opcode 0.

        Parameters
        ----------
        payload : :class:`~pincer.core.dispatch.GatewayDispatch`
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        await self.process_event(payload.event_name.lower(), payload, gateway)

    async def payload_event_handler(
        self, gateway: Gateway, payload: GatewayDispatch
    ):
        """|coro|

        Special event which activates the on_payload event.

        Parameters
        ----------
        payload : :class:`~pincer.core.dispatch.GatewayDispatch`
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        await self.process_event("payload", payload, gateway)

    @overload
    async def create_guild(
        self,
        *,
        name: str,
        region: Optional[str] = None,
        icon: Optional[str] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        roles: Optional[List[Role]] = None,
        channels: Optional[List[Channel]] = None,
        afk_channel_id: Optional[Snowflake] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[Snowflake] = None,
        system_channel_flags: Optional[int] = None,
    ) -> Guild:
        """Creates a guild.

        Parameters
        ----------
        name : :class:`str`
            Name of the guild (2-100 characters)
        region : Optional[:class:`str`]
            Voice region id (deprecated) |default| :data:`None`
        icon : Optional[:class:`str`]
            base64 128x128 image for the guild icon |default| :data:`None`
        verification_level : Optional[:class:`int`]
            Verification level |default| :data:`None`
        default_message_notifications : Optional[:class:`int`]
            Default message notification level |default| :data:`None`
        explicit_content_filter : Optional[:class:`int`]
            Explicit content filter level |default| :data:`None`
        roles : Optional[List[:class:`~pincer.objects.guild.role.Role`]]
            New guild roles |default| :data:`None`
        channels : Optional[List[:class:`~pincer.objects.guild.channel.Channel`]]
            New guild's channels |default| :data:`None`
        afk_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID for AFK channel |default| :data:`None`
        afk_timeout : Optional[:class:`int`]
            AFK timeout in seconds |default| :data:`None`
        system_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The ID of the channel where guild notices such as welcome
            messages and boost events are posted |default| :data:`None`
        system_channel_flags : Optional[:class:`int`]
            System channel flags |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
            The created guild
        """
        ...

    async def create_guild(self, name: str, **kwargs) -> Guild:
        g = await self.http.post("guilds", data={"name": name, **kwargs})
        return await self.get_guild(g["id"])

    async def get_guild_template(self, code: str) -> GuildTemplate:
        """|coro|
        Retrieves a guild template by its code.

        Parameters
        ----------
        code : :class:`str`
            The code of the guild template

        Returns
        -------
        :class:`~pincer.objects.guild.template.GuildTemplate`
            The guild template
        """
        return GuildTemplate.from_dict(
            await self.http.get(f"guilds/templates/{code}")
        )

    async def create_guild_from_template(
        self, template: GuildTemplate, name: str, icon: Optional[str] = None
    ) -> Guild:
        """|coro|
        Creates a guild from a template.

        Parameters
        ----------
        template : :class:`~pincer.objects.guild.template.GuildTemplate`
            The guild template
        name : :class:`str`
            Name of the guild (2-100 characters)
        icon : Optional[:class:`str`]
            base64 128x128 image for the guild icon |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
            The created guild
        """
        return Guild.from_dict(
            await self.http.post(
                f"guilds/templates/{template.code}",
                data={"name": name, "icon": icon},
            )
        )

    async def wait_for(
        self,
        event_name: str,
        check: CheckFunction = None,
        timeout: Optional[float] = None,
    ):
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.
        check : CheckFunction
            This function only returns a value if this return true.
        timeout: Optional[float]
            Amount of seconds before timeout.

        Returns
        ------
        Any
            What the Discord API returns for this event.
        """
        return await self.event_mgr.wait_for(event_name, check, timeout)

    def loop_for(
        self,
        event_name: str,
        check: CheckFunction = None,
        iteration_timeout: Optional[float] = None,
        loop_timeout: Optional[float] = None,
    ):
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.
        check : Callable[[Any], bool], default=None
            This function only returns a value if this return true.
        iteration_timeout: Union[float, None]
            Amount of seconds before timeout. Timeouts are for each loop.
        loop_timeout: Union[float, None]
            Amount of seconds before the entire loop times out. The generator
            will only raise a timeout error while it is waiting for an event.

        Yields
        ------
        Any
            What the Discord API returns for this event.
        """
        return self.event_mgr.loop_for(
            event_name, check, iteration_timeout, loop_timeout
        )

    async def get_guild(self, guild_id: int, with_count: bool = False) -> Guild:
        """|coro|

        Fetch a guild object by the guild identifier.

        Parameters
        ----------
        with_count: :class:bool
            Whether to include the member count in the guild object.
            Default to `False`

        guild_id : :class:`int`
            The id of the guild which should be fetched from the Discord
            gateway.

        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
            The guild object.
        """
        return await Guild.from_id(self, guild_id, with_count)

    async def get_user(self, _id: int) -> User:
        """|coro|

        Fetch a User from its identifier

        Parameters
        ----------
        _id : :class:`int`
            The id of the user which should be fetched from the Discord
            gateway.

        Returns
        -------
        :class:`~pincer.objects.user.user.User`
            The user object.
        """
        return await User.from_id(self, _id)

    async def get_role(self, guild_id: int, role_id: int) -> Role:
        """|coro|

        Fetch a role object by the role identifier.

        guild_id: :class:`int`
            The guild in which the role resides.

        role_id: :class:`int`
            The id of the guild which should be fetched from the Discord
            gateway.

        Returns
        -------
        :class:`~pincer.objects.guild.role.Role`
            A Role object.
        """
        return await Role.from_id(self, guild_id, role_id)

    async def get_channel(self, _id: int) -> Channel:
        """|coro|
        Fetch a Channel from its identifier. The ``get_dm_channel`` method from
        :class:`~pincer.objects.user.user.User` should be used if you need to
        create a dm_channel; using the ``send()`` method from
        :class:`~pincer.objects.user.user.User` is preferred.

        Parameters
        ----------
        _id: :class:`int`
            The id of the user which should be fetched from the Discord
            gateway.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            A Channel object.
        """
        return await Channel.from_id(self, _id)

    async def get_message(
        self, _id: Snowflake, channel_id: Snowflake
    ) -> UserMessage:
        """|coro|
        Creates a UserMessage object

        Parameters
        ----------
        _id: :class:`~pincer.utils.snowflake.Snowflake`
            ID of the message that is wanted.
        channel_id : int
            ID of the channel the message is in.

        Returns
        -------
        :class:`~pincer.objects.message.user_message.UserMessage`
            The message object.
        """

        return await UserMessage.from_id(self, _id, channel_id)

    async def get_webhook(
        self, id: Snowflake, token: Optional[str] = None
    ) -> Webhook:
        """|coro|
        Fetch a Webhook from its identifier.

        Parameters
        ----------
        id: :class:`int`
            The id of the webhook which should be
            fetched from the Discord gateway.
        token: Optional[:class:`str`]
            The webhook token.

        Returns
        -------
        :class:`~pincer.objects.guild.webhook.Webhook`
            A Webhook object.
        """
        return await Webhook.from_id(self, id, token)

    async def get_current_user(self) -> User:
        """|coro|
        The user object of the requester's account.

        For OAuth2, this requires the ``identify`` scope,
        which will return the object *without* an email,
        and optionally the ``email`` scope,
        which returns the object *with* an email.

        Returns
        -------
        :class:`~pincer.objects.user.user.User`
        """
        return User.from_dict(await self.http.get("users/@me"))

    async def modify_current_user(
        self, username: Optional[str] = None, avatar: Optional[File] = None
    ) -> User:
        """|coro|
        Modify the requester's user account settings

        Parameters
        ----------
        username : Optional[:class:`str`]
            user's username,
            if changed may cause the user's discriminator to be randomized.
            |default| :data:`None`
        avatar : Optional[:class:`File`]
            if passed, modifies the user's avatar
            a data URI scheme of JPG, GIF or PNG
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.user.user.User`
            Current modified user
        """

        avatar = avatar.uri if avatar else avatar

        user = await self.http.patch(
            "users/@me", remove_none({"username": username, "avatar": avatar})
        )
        return User.from_dict(user)

    async def get_current_user_guilds(
        self,
        before: Optional[Snowflake] = None,
        after: Optional[Snowflake] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[Guild]:
        """|coro|
        Returns a list of partial guild objects the current user is a member of.
        Requires the ``guilds`` OAuth2 scope.

        Parameters
        ----------
        before : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            get guilds before this guild ID
        after : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            get guilds after this guild ID
        limit : Optional[:class:`int`]
                max number of guilds to return (1-200) |default| :data:`200`

        Yields
        ------
        :class:`~pincer.objects.guild.guild.Guild`
            A Partial Guild that the user is in
        """
        guilds = await self.http.get(
            "users/@me/guilds?"
            + (f"{before=}&" if before else "")
            + (f"{after=}&" if after else "")
            + (f"{limit=}&" if limit else "")
        )

        for guild in guilds:
            yield Guild.from_dict(guild)

    async def leave_guild(self, _id: Snowflake):
        """|coro|
        Leave a guild.

        Parameters
        ----------
        _id : :class:`~pincer.utils.snowflake.Snowflake`
            the id of the guild that the bot will leave
        """
        await self.http.delete(f"users/@me/guilds/{_id}")
        self._client.guilds.pop(_id, None)

    async def create_group_dm(
        self, access_tokens: List[str], nicks: Dict[Snowflake, str]
    ) -> GroupDMChannel:
        """|coro|
        Create a new group DM channel with multiple users.
        DMs created with this endpoint will not be shown in the Discord client

        Parameters
        ----------
        access_tokens : List[:class:`str`]
            access tokens of users that have
            granted your app the ``gdm.join`` scope

        nicks : Dict[:class:`~pincer.utils.snowflake.Snowflake`, :class:`str`]
            a dictionary of user ids to their respective nicknames

        Returns
        -------
        :class:`~pincer.objects.guild.channel.GroupDMChannel`
            group DM channel created
        """
        channel = await self.http.post(
            "users/@me/channels",
            {"access_tokens": access_tokens, "nicks": nicks},
        )

        return GroupDMChannel.from_dict(channel)

    async def get_connections(self) -> AsyncIterator[Connection]:
        """|coro|
        Returns a list of connection objects.
        Requires the ``connections`` OAuth2 scope.

        Yields
        -------
        :class:`~pincer.objects.user.connection.Connections`
            the connection objects
        """
        connections = await self.http.get("users/@me/connections")
        for conn in connections:
            yield Connection.from_dict(conn)

    async def sticker_packs(self) -> AsyncIterator[StickerPack]:
        """|coro|
        Yields sticker packs available to Nitro subscribers.

        Yields
        ------
        :class:`~pincer.objects.message.sticker.StickerPack`
            a sticker pack
        """
        packs = await self.http.get("sticker-packs")
        for pack in packs:
            yield StickerPack.from_dict(pack)

    async def create_stage(
        self,
        channel_id: int,
        topic: str,
        privacy_level: Optional[PrivacyLevel] = None,
        reason: Optional[str] = None,
    ) -> StageInstance:
        """|coro|

        Parameters
        ----------
        channel_id : :class:`int`
            The id of the Stage channel
        topic : :class:`str`
            The topic of the Stage instance (1-120 characters)
        privacy_level : Optional[:class:`~pincer.objects.guild.stage.PrivacyLevel`]
            The privacy level of the Stage instance (default :data:`GUILD_ONLY`)
        reason : Optional[:class:`str`]
            The reason for creating the Stage instance

        Returns
        -------
        :class:`~pincer.objects.guild.stage.StageInstance`
            The Stage instance created
        """

        data = {
            "channel_id": channel_id,
            "topic": topic,
            "privacy_level": privacy_level,
        }

        return await self.http.post(  # type: ignore
            "stage-instances", remove_none(data), headers={"reason": reason}
        )

    async def get_stage(self, _id: int) -> StageInstance:
        """|coro|
        Gets the stage instance associated with the Stage channel, if it exists

        Parameters
        ----------
        _id : int
            The ID of the stage to get

        Returns
        -------
        :class:`~pincer.objects.guild.stage.StageInstance`
            The stage instance
        """
        return await StageInstance.from_id(self, _id)

    async def modify_stage(
        self,
        _id: int,
        topic: Optional[str] = None,
        privacy_level: Optional[PrivacyLevel] = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Updates fields of an existing Stage instance.
        Requires the user to be a moderator of the Stage channel.

        Parameters
        ----------
        _id : int
            The ID of the stage to modify
        topic : Optional[:class:`str`]
            The topic of the Stage instance (1-120 characters)
        privacy_level : Optional[:class:`~pincer.objects.guild.stage.PrivacyLevel`]
            The privacy level of the Stage instance
        reason : Optional[:class:`str`]
            The reason for the modification
        """

        await self.http.patch(
            f"stage-instances/{_id}",
            remove_none({"topic": topic, "privacy_level": privacy_level}),
            headers={"reason": reason},
        )

    async def delete_stage(self, _id: int, reason: Optional[str] = None):
        """|coro|
        Deletes the Stage instance.
        Requires the user to be a moderator of the Stage channel.

        Parameters
        ----------
        _id : int
            The ID of the stage to delete
        reason : Optional[:class:`str`]
            The reason for the deletion
        """
        await self.http.delete(
            f"stage-instances/{_id}", headers={"reason": reason}
        )

    async def crosspost_message(
        self, channel_id: int, message_id: int
    ) -> UserMessage:
        """|coro|
        Crosspost a message in a News Channel to following channels.

        This endpoint requires the ``SEND_MESSAGES`` permission,
        if the current user sent the message, or additionally the
        ``MANAGE_MESSAGES`` permission, for all other messages,
        to be present for the current user.

        Parameters
        ----------
        channel_id : int
            ID of the news channel that the message is in.
        message_id : int
            ID of the message to crosspost.

        Returns
        -------
        :class:`~pincer.objects.message.UserMessage`
            The crossposted message
        """

        return await self._http.post(
            f"channels/{channel_id}/{message_id}/crosspost"
        )


Bot = Client
