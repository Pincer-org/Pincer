# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from inspect import isasyncgenfunction, _empty
from typing import Dict, Any
from typing import TYPE_CHECKING


from ..commands import ChatCommandHandler
from ..core.dispatch import GatewayDispatch
from ..objects import Interaction, MessageContext, AppCommandType
from ..utils import MISSING, should_pass_cls, Coro, should_pass_ctx
from ..utils import get_index
from ..utils.conversion import construct_client_dict
from ..utils.signature import get_signature_and_params

if TYPE_CHECKING:
    from typing import List, Tuple


_log = logging.getLogger(__name__)


async def interaction_response_handler(
    self,
    command: Coro,
    context: MessageContext,
    interaction: Interaction,
    args: List[Any],
    kwargs: Dict[str, Any],
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
    self, interaction: Interaction, context: MessageContext, command: Coro
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
    self.throttler.handle(context)

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

    kwargs = {**defaults, **params}

    await interaction_response_handler(
        self, command, context, interaction, args, kwargs
    )


async def interaction_create_middleware(
    self, payload: GatewayDispatch
) -> Tuple[str, Interaction]:
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
    Tuple[:class:`str`, :class:`~pincer.objects.app.interactions.Interaction`]
        ``on_interaction_create`` and an ``Interaction``
    """
    interaction: Interaction = Interaction.from_dict(
        construct_client_dict(self, payload.data)
    )
    command = ChatCommandHandler.register.get(interaction.data.name)

    if command:
        context = interaction.convert_to_message_context(command)

        try:
            await interaction_handler(self, interaction, context, command.call)
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
                        {params[-1]: e},
                    )
                else:
                    raise e
            else:
                raise e

    return "on_interaction_create", interaction


def export() -> Coro:
    return interaction_create_middleware
