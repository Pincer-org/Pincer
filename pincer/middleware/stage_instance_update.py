# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a stage instance is updated."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import StageInstance
from ..utils import Coro, replace

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def stage_instance_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_stage_instance_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the stage instance update event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.stage.StageInstance`]
        ``on_stage_instance_update`` and a ``StageInstance``
    """

    stage = StageInstance.from_dict(payload.data)

    guild = self.guilds.get(stage.guild_id)
    if guild:
        guild.stage_instances = replace(
            lambda _stage: _stage.id == stage.id, guild.stage_instances, stage
        )

    return "on_stage_instance_update", stage


def export() -> Coro:
    return stage_instance_update_middleware
