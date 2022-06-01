# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass


@dataclass(repr=False)
class GatewayConfig:
    """This file is to make maintaining the library and its gateway
    configuration easier. Leave compression blank for no compression.
    """

    MAX_RETRIES: int = 5
    version: int = 9
    encoding: str = "json"
    compression: str = "zlib-payload"

    @classmethod
    def make_uri(cls, uri) -> str:
        """
        Returns
        -------
        :class:`str`:
            The GatewayConfig's uri.
        """
        return (
            f"{uri}" f"?v={cls.version}" f"&encoding={cls.encoding}"
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
