# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a stage instance is deleted or closed."""
from ..core.dispatch import GatewayDispatch
from ..objects import StageInstance
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


def stage_instance_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_stage_instance_delete`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the stage instance delete event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.stage.StageInstance`]]
        ``on_stage_instance_delete`` and a ``StageInstance``
    """

    return "on_stage_instance_delete", [
        StageInstance.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return stage_instance_delete_middleware
