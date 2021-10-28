# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

import logging
from inspect import isasyncgenfunction, getfullargspec
from typing import Dict, Any

from pincer.utils import get_index
from ..commands import ChatCommandHandler
from ..core.dispatch import GatewayDispatch
from ..objects import Interaction, MessageContext
from ..utils import MISSING, should_pass_cls, Coro, should_pass_ctx
from ..utils.conversion import construct_client_dict
from ..utils.signature import get_params, get_signature_and_params

_log = logging.getLogger(__name__)


async def interaction_response_handler(
        self,
        command: Coro,
        context: MessageContext,
        interaction: Interaction,
        kwargs: Dict[str, Any]
):
    """
    Handle any coroutine as a command.

    :param self:
        The current client.

    :param command:
        The coroutine which will be seen as a command.

    :param context:
        The context of the command.

    :param interaction:
        The interaction which is linked to the command.

    :param kwargs:
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

        async for msg in message:
            if interaction.has_replied:
                await interaction.followup(msg)
            else:
                await interaction.reply(msg)
    else:
        message = await command(**kwargs)
        if not interaction.has_replied:
            await interaction.reply(message)


async def interaction_handler(
        self,
        interaction: Interaction,
        context: MessageContext,
        command: Coro
):
    """
    Processes an interaction.

    :param self:
        The current client.

    :param interaction:
        The interaction which is linked to the command.

    :param context:
        The context of the command.

    :param command:
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


async def interaction_create_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_interaction``, which handles command
    execution.

    :param self:
        The current client.

    :param payload:
        The data received from the interaction event.
    """

    interaction: Interaction = Interaction.from_dict(
        construct_client_dict(self, payload.data)
    )
    await interaction.build()
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
