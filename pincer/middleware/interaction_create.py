# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from inspect import isasyncgenfunction, getfullargspec

from ..utils.extraction import get_index

if TYPE_CHECKING:
    from typing import Union, Dict, Any, Tuple, List

    from ..utils.types import Coro
    from ..utils.types import MISSING
    from ..objects.message.file import File
    from ..commands import ChatCommandHandler
    from ..objects.message.embed import Embed
    from ..core.dispatch import GatewayDispatch
    from ..objects.message.message import Message
    from ..objects.app.interactions import Interaction
    from ..objects.message.context import MessageContext
    from ..utils.conversion import construct_client_dict
    from ..objects.app.interactions import InteractionFlags
    from ..utils.insertion import should_pass_cls, should_pass_ctx
    from ..utils.signature import get_params, get_signature_and_params

PILLOW_IMPORT = True

try:
    from PIL.Image import Image
except (ModuleNotFoundError, ImportError):
    PILLOW_IMPORT = False

_log = logging.getLogger(__name__)


def convert_message(self, message: Union[Embed, Message, str]) -> Message:
    """Converts a message to a Message object

    Parameters
    ----------
    message : Union[:class:`~pincer.objects.message.embed.Embed`, :class:`~pincer.objects.message.message.Message`, :class:`str`]
        Message to convert
    """  # noqa: E501
    if isinstance(message, Embed):
        message = Message(embeds=[message])
    elif PILLOW_IMPORT and isinstance(message, (File, Image)):
        message = Message(attachments=[message])
    elif not isinstance(message, Message):
        message = Message(message) if message else Message(
            self.received_message,
            flags=InteractionFlags.EPHEMERAL
        )
    return message


async def reply(self, interaction: Interaction, message: Message):
    """|coro|

    Sends a reply to an interaction.

    Parameters
    ----------
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction from whom the reply is.
    message : :class:`~pincer.objects.message.message.Message`
        The message to reply with.
    """

    content_type, data = message.serialize()

    await self.http.post(
        f"interactions/{interaction.id}/{interaction.token}/callback",
        data,
        content_type=content_type
    )


async def interaction_response_handler(
        self,
        command: Coro,
        context: MessageContext,
        interaction: Interaction,
        kwargs: Dict[str, Any]
):
    """|coro|

    Handle any coroutine as a command.

    Parameters
    ----------
    command : :data:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    \\*\\*kwargs :
        The arguments to be passed to the command.
    """
    if should_pass_cls(command):
        cls_keyword = getfullargspec(command).args[0]
        kwargs[cls_keyword] = ChatCommandHandler.managers[command.__module__]

    sig, params = get_signature_and_params(command)
    if should_pass_ctx(sig, params):
        kwargs[params[0]] = context

    if isasyncgenfunction(command):
        message = command(**kwargs)
        started = False

        async for msg in message:
            msg = convert_message(self, msg)

            if started:
                await self.http.post(
                    f"webhooks/{interaction.application_id}"
                    f"/{interaction.token}",
                    msg.to_dict().get("data")
                )
            else:
                started = True
                await reply(self, interaction, msg)
    else:
        message = await command(**kwargs)
        await reply(self, interaction, convert_message(self, message))


async def interaction_handler(
        self,
        interaction: Interaction,
        context: MessageContext,
        command: Coro
):
    """|coro|

    Processes an interaction.

    Parameters
    ----------
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    command : :data:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    """
    self.throttler.handle(context)

    defaults = {param: None for param in get_params(command)}
    params = {}

    if interaction.data.options is not MISSING:
        params = {
            opt.name: opt.value for opt in interaction.data.options
        }

    kwargs = {**defaults, **params}

    await interaction_response_handler(self, command, context, interaction,
                                       kwargs)


async def interaction_create_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[Interaction]]:
    """Middleware for ``on_interaction``, which handles command
    execution.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the interaction event.

    Raises
    ------
    e
        Generic try except on ``await interaction_handler`` and
        ``if 0 < len(params) < 3``

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.app.interactions.Interaction`]]
        ``on_interaction_create`` and an ``Interaction``
    """  # noqa: E501
    interaction: Interaction = Interaction.from_dict(
        construct_client_dict(self, payload.data)
    )
    command = ChatCommandHandler.register.get(interaction.data.name)

    if command:
        context = interaction.convert_to_message_context(command)

        try:
            await interaction_handler(self, interaction, context,
                                      command.call)
        except Exception as e:
            if coro := get_index(self.get_event_coro("on_command_error"), 0):
                params = get_signature_and_params(coro)[1]

                # Check if a context or error var has been passed.
                if 0 < len(params) < 3:
                    await interaction_response_handler(
                        self,
                        coro,
                        context,
                        interaction,
                        # Always take the error parameter its name.
                        {params[(len(params) - 1) or 0]: e}
                    )
                else:
                    raise e
            else:
                raise e

    return "on_interaction_create", [interaction]


def export() -> Coro:
    return interaction_create_middleware
