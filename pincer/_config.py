# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional


@dataclass
class GatewayConfig:
    """This file is to make maintaining the library its gateway
    configuration easier.
    """
    socket_base_url: str = "wss://gateway.discord.gg/"
    version: int = 9
    encoding: str = "json"
    compression: Optional[str] = "zlib-stream"

    @classmethod
    def uri(cls) -> str:
        """
        Returns
        -------
        :class:`str`:
            The GatewayConfig's uri.
        """
        return (
            f"{cls.socket_base_url}"
            f"?v={cls.version}"
            f"&encoding={cls.encoding}"
        ) + f"&compress={cls.compression}" * cls.compressed()

    @classmethod
    def compressed(cls) -> bool:
        """
        Returns
        -------
        :class:`bool`:
            Whether the Gateway should compress payloads or not.
        """
        return cls.compression in ["zlib-stream", "zlib-payload"]
