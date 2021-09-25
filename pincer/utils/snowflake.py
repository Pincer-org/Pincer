# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


class Snowflake(int):
    """
    Discord utilizes Twitter's snowflake format for uniquely
    identifiable descriptors (IDs).

    These IDs are guaranteed to be unique across all of Discord,
    except in some unique scenarios in which child objects
    share their parent's ID.

    Because Snowflake IDs are up to 64 bits in size (e.g. a uint64),
    they are always returned as strings in the HTTP API
    to prevent integer overflows in some languages.
    """
    @classmethod
    def from_string(cls, string: str):
        """
        Initialize a new Snowflake from a string.

        :param string:
            The snowflake as a string.
        """
        return Snowflake(int(string))

    @property
    def timestamp(self) -> int:
        """
        Milliseconds since Discord Epoch,
        the first second of 2015 or 14200704000000
        """
        return self >> 22

    @property
    def worker_id(self) -> int:
        """Internal worker ID"""
        return (self >> 17) % 16

    @property
    def process_id(self) -> int:
        """Internal process ID"""
        return (self >> 12) % 16

    @property
    def increment(self) -> int:
        """
        For every ID that is generated on that process,
        this number is incremented
        """
        return self % 2048
