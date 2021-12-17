# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a stage instance is created."""
from ..core.dispatch import GatewayDispatch
from ..objects import StageInstance
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def stage_instance_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_stage_instance_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the stage instance create event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.stage.StageInstance`]
        ``on_stage_instance_create`` and a ``StageInstance``
    """

    stage = StageInstance.from_dict(construct_client_dict(self, payload.data))

    guild = self.guilds.get(stage.guild_id)
    if guild:
        guild.stage_instances.append(stage)

    return "on_stage_instance_create", stage


def export() -> Coro:
    return stage_instance_create_middleware
