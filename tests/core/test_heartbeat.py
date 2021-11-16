# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from unittest.mock import AsyncMock, Mock, patch

import pytest

from pincer.core.heartbeat import Heartbeat
from tests._utils import assert_not_raises


@pytest.fixture
def web_socket_client_protocol():
    return AsyncMock()


class TestHeartbeat:
    @staticmethod
    def test_get():
        assert Heartbeat.get() == 0

    @pytest.mark.asyncio
    async def test_handle_hello(self, web_socket_client_protocol):
        payload = Mock()
        payload.data.get.return_value = 1
        with patch("pincer.core.heartbeat.Heartbeat"):
            await Heartbeat.handle_hello(web_socket_client_protocol, payload)
        web_socket_client_protocol.send.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_handle_heartbeat(self, web_socket_client_protocol):
        await Heartbeat.handle_heartbeat(web_socket_client_protocol, "GARBAGE")
        web_socket_client_protocol.send.assert_awaited_once()

    @staticmethod
    def test_update_sequence():
        with assert_not_raises():
            Heartbeat.update_sequence(42)
