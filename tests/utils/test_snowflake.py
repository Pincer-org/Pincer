import pytest

from pincer.utils import Snowflake


class TestSnowflake:

    def test_boundaries(self):
        with pytest.raises(ValueError):
            Snowflake(9223372036854775808)
            Snowflake(0)

    def test_conversions(self):
        assert Snowflake(1) == 1
        assert Snowflake("1") == 1

    def test_timestamp(self):
        # values from: https://discord.com/developers/docs/reference#snowflakes.
        x = Snowflake(175928847299117063)
        assert x.timestamp == 41944705796
        assert x.unix == 1462015105796
