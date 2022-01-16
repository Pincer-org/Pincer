# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    from .snowflake import Snowflake


def calculate_shard_id(guild_id: Union[Snowflake, int], num_shards: int) -> int:
    """Calculates the shard receiving the events for a specified guild

    Parameters
    ----------
    guild_id : Optional[~pincer.utils.snowflake.Snowflake]
        The guild_id of the shard to look for
    num_shards : Optional[int]
        The number of shards.
    """
    return (guild_id >> 22) % num_shards
