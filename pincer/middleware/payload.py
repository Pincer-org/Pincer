# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when basically anything is received from gateway"""

from ..core.dispatch import GatewayDispatch


async def payload_middleware(self, payload: GatewayDispatch):
    return "on_payload", payload


def export():
    return payload_middleware
