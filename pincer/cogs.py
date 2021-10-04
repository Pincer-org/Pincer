# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class Cog:
    def __init__(self, client: Client):
        self.client: Client = client
