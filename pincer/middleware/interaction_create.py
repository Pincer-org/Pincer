# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from contextlib import suppress
from inspect import isasyncgenfunction, _empty
from typing import Dict, Any
from typing import TYPE_CHECKING

from ..commands import ChatCommandHandler, ComponentHandler, hash_app_command_params
from ..exceptions import InteractionDoesNotExist
from ..objects import Interaction, MessageContext, AppCommandType, InteractionType
from ..utils import MISSING, should_pass_cls, Coro, should_pass_ctx
from ..utils import get_index
from ..utils.conversion import construct_client_dict
from ..utils.signature import get_signature_and_params

if TYPE_CHECKING:
    from typing import List, Tuple
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch

_log = logging.getLogger(__name__)


def get_command_from_registry(interaction: Interaction):
    """
    Search for a command in ChatCommandHandler.register and return it if it exists

    Parameters
    ---------
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction to get the command from

    Raises
    ------
    :class:`~pincer.exceptions.InteractionDoesNotExist`
        The command is not registered
    """

    with suppress(KeyError):
        return ChatCommandHandler.register[hash_app_command_params(
            interaction.data.name,
            MISSING,
            interaction.data.type
        )]

    with suppress(KeyError):
        return ChatCommandHandler.register[hash_app_command_params(
            interaction.data.name,
            interaction.guild_id,
            interaction.data.type
        )]

    raise InteractionDoesNotExist(
        f"No command is registered for {interaction.data.name} with type"
        f"{interaction.data.type}"
    )


def get_call(self: Client, interaction: Interaction):
    if interaction.type == InteractionType.APPLICATION_COMMAND:
        command = get_command_from_registry(interaction)
        if command is None:
            return None
        # Only application commands can be throttled
        self.throttler.handle(command)
        return command.call
    elif interaction.type == InteractionType.MESSAGE_COMPONENT:
        return ComponentHandler.register.get(interaction.data.custom_id)
    elif interaction.type == InteractionType.AUTOCOMPLETE:
        raise NotImplementedError(
            "Handling for autocomplete is not implemented"
        )


async def interaction_response_handler(
    command: Coro,
    context: MessageContext,
    interaction: Interaction,
    args: List[Any],
    kwargs: Dict[str, Any]
):
    """|coro|

    Handle any coroutine as a command.

    Parameters
    ----------
    command : :class:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    \\*\\*kwargs :
        The arguments to be passed to the command.
    """
    sig, params = get_signature_and_params(command)
    if should_pass_ctx(sig, params):
        args.insert(0, context)

    if should_pass_cls(command):
        args.insert(0, ChatCommandHandler.managers[command.__module__])

    if isasyncgenfunction(command):
        message = command(*args, **kwargs)

        async for msg in message:
            if interaction.has_replied:
                await interaction.followup(msg)
            else:
                await interaction.reply(msg)
    else:
        message = await command(*args, **kwargs)
        if not interaction.has_replied:
            await interaction.reply(message)


async def interaction_handler(
    interaction: Interaction, context: MessageContext, command: Coro
):
    """|coro|

    Processes an interaction.

    Parameters
    ----------
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    command : :class:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    """
    sig, _ = get_signature_and_params(command)

    defaults = {
        key: value.default
        for key, value in sig.items()
        if value.default is not _empty
    }
    params = {}

    if interaction.data.options is not MISSING:
        params = {opt.name: opt.value for opt in interaction.data.options}

    args = []

    if interaction.data.type == AppCommandType.USER:
        # Add User and Member args
        user = next(iter(interaction.data.resolved.users.values()))

        if members := interaction.data.resolved.members:
            member = next(iter(members.values()))
            member.set_user_data(user)
            args.append(member)
        else:
            args.append(user)

    elif interaction.data.type == AppCommandType.MESSAGE:
        # Add Message to args
        args.append(next(iter(interaction.data.resolved.messages.values())))

    if interaction.data.values:
        args.append(interaction.data.values)

    kwargs = {**defaults, **params}

    await interaction_response_handler(
        command, context, interaction, args, kwargs
    )


async def interaction_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str, Interaction]:
    """Middleware for ``on_interaction``, which handles command
    execution.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the interaction event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Raises
    ------
    e
        Generic try except on ``await interaction_handler`` and
        ``if 0 < len(params) < 3``

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.app.interactions.Interaction`]
        ``on_interaction_create`` and an ``Interaction``
    """
    interaction: Interaction = Interaction.from_dict(
        construct_client_dict(self, payload.data)
    )

    call = get_call(self, interaction)
    context = interaction.get_message_context()

    try:
        await interaction_handler(interaction, context, call)
    except Exception as e:
        if coro := get_index(self.get_event_coro("on_command_error"), 0):
            params = get_signature_and_params(coro)[1]

            # Check if a context or error var has been passed.
            if 0 < len(params) < 3:
                await interaction_response_handler(
                    coro,
                    context,
                    interaction,
                    # Always take the error parameter its name.
                    {params[-1]: e},
                )
            else:
                raise e
        else:
            raise e

    return "on_interaction_create", interaction


def export() -> Coro:
    return interaction_create_middleware
