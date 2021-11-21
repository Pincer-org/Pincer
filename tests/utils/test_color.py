import pytest
from pincer.utils import Color


class TestSnowflake:

    @staticmethod
    def test_conversion():
        c = Color("#aabb01")
        assert c.r == 170
        assert c.g == 187
        assert c.b == 1
        assert c.hex == 'aabb01'

    @staticmethod
    def test_invalids():
        with pytest.raises(ValueError):
            Color(-1)
            Color(16777216)
            Color("12345")
            Color("1234567")
            Color("agbbcc")
