# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

from json import dumps, loads
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Union


class GatewayDispatch:
    """Represents a websocket message.

    Attributes
    ----------
    op: :class:`int`
        The discord opcode which represents what the message means.
    data: Optional[Union[:class:`int`, Dict[:class:`str`, Any]]]
        The event data that has been sent/received.
    seq: Optional[:class:`int`]
        The sequence number of a message, which can be used
        for resuming sessions and heartbeats.
    event_name: Optional[:class:`str`]
        The event name for the payload.
    """

    def __init__(
            self,
            op: int,
            data: Optional[Union[int, Dict[str, Any]]],
            seq: Optional[int] = None,
            name: Optional[str] = None
    ):
        self.op: int = op
        self.data: Optional[Union[int, Dict[str, Any]]] = data
        self.seq: Optional[int] = seq
        self.event_name: Optional[str] = name

    def __str__(self) -> str:
        return dumps(
            dict(
                op=self.op,
                d=self.data,
                s=self.seq,
                t=self.event_name
            )
        )

    @classmethod
    def from_string(cls, payload: str) -> GatewayDispatch:
        """Parses a given payload from a string format
        and returns a GatewayDispatch.

        Parameters
        ----------
        payload : :class:`str`
            The payload to parse.

        Returns
        -------
        :class:`~pincer.core.dispatch.GatewayDispatch`
            The new class.
        """
        payload: Dict[str, Union[int, str, Dict[str, Any]]] = loads(payload)
        return cls(
            payload.get("op"),
            payload.get("d"),
            payload.get("s"),
            payload.get("t")
        )
