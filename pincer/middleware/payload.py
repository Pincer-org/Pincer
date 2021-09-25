# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from ..core.dispatch import GatewayDispatch


async def payload_middleware(self, payload: GatewayDispatch):
    """Invoked when basically anything is received from gateway.."""
    return "on_payload", [payload]


def export():
    """Export the middleware"""
    return payload_middleware
