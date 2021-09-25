# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

from json import dumps, loads
from typing import Optional, Union, Dict, Any


class GatewayDispatch:
    """Represents a websocket message."""

    def __init__(
            self,
            op: int,
            data: Optional[Union[int, Dict[str, Any]]],
            seq: Optional[int] = None,
            name: Optional[str] = None
    ):
        """
        Instantiate a new GatewayDispatch object.

        :param op:
            The discord opcode which represents what the message means.

        :param data:
            The event data that has been sent/received.

        :param seq:
            The sequence number of a message, which can be used
            for resuming sessions and heartbeats.

        :param name:
            The event name for the payload.
        """
        self.op: int = op
        self.data: Optional[Union[int, Dict[str, Any]]] = data
        self.seq: Optional[int] = seq
        self.event_name: Optional[str] = name

    def __str__(self) -> str:
        """
        :return
            The string representation of the GatewayDispatch object.

        This can be used to send a websocket message to the gateway.
        """
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
        """
        Parses a given payload from a string format
            and returns a GatewayDispatch.

        :param payload:
            The payload to parse.

        :return:
            A proper GatewayDispatch object.
        """
        payload: Dict[str, Union[int, str, Dict[str, Any]]] = loads(payload)
        return cls(
            payload.get("op"),
            payload.get("d"),
            payload.get("s"),
            payload.get("t")
        )
