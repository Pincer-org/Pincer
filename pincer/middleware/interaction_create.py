# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Union
from asyncio import sleep
from inspect import isasyncgenfunction
import logging

from ..commands import ChatCommandHandler
from ..exceptions import RateLimitError
from ..core.dispatch import GatewayDispatch
from ..objects import Interaction, Embed, Message, InteractionFlags
from ..utils import MISSING, should_pass_cls, Coro
from ..utils.extraction import get_params

_log = logging.getLogger(__name__)


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
        payload.data | {"_client": self, "_http": self.http}
    )

    command = ChatCommandHandler.register.get(interaction.data.name)

    if command:
        defaults = {param: None for param in get_params(command.call)}
        params = {}

        if interaction.data.options is not MISSING:
            params = {
                opt.name: opt.value for opt in interaction.data.options
            }

        kwargs = {**defaults, **params}

        if should_pass_cls(command.call):
            kwargs["self"] = self

        if isasyncgenfunction(command.call):
            message = command.call(**kwargs)
            started = False

            async for msg in message:

                msg = convert_message(self, msg)
                if started:
                    try:
                        await self.http.post(
                            f"webhooks/{interaction.application_id}"
                            f"/{interaction.token}",
                            msg.to_dict().get("data")
                        )
                    except RateLimitError as e:
                        _log.exception(
                            f"RateLimitError: {e}."
                            f" Retrying in {e.json.get('retry_after', 40)}"
                            f" seconds"
                        )

                        await sleep(e.json.get("retry_after", 40))
                        await self.http.post(
                            f"webhooks/{interaction.application_id}"
                            f"/{interaction.token}",
                            msg.to_dict().get("data")
                        )

                else:
                    started = True

                    await self.http.post(
                        f"interactions/{interaction.id}"
                        f"/{interaction.token}/callback",
                        msg.to_dict()
                    )
                await sleep(0.3)
        else:
            message = await command.call(**kwargs)
            message = convert_message(self, message)

            await self.http.post(
                f"interactions/{interaction.id}/{interaction.token}/callback",
                message.to_dict()
            )

    return "on_interaction_create", [interaction]


def convert_message(self, message: Union[Embed, Message, str]) -> Message:
    """Converts a message to a Message object"""
    if isinstance(message, Embed):
        message = Message(embeds=[message])
    elif not isinstance(message, Message):
        message = Message(message) if message else Message(
            self.received_message,
            flags=InteractionFlags.EPHEMERAL
        )
    return message


def export() -> Coro:
    return interaction_create_middleware
