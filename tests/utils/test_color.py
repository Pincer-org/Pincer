import pytest
from pincer.utils import Color


class TestSnowflake:

    def test_conversion(self):
        c = Color("#aabbcc")
        assert c.r == 170
        assert c.g == 187
        assert c.b == 204
        assert c.hex == 'aabbcc'

    def test_invalids(self):
        with pytest.raises(ValueError):
            Color(-1)
            Color(16777216)
            Color("12345")
            Color("1234567")
            Color("agbbcc")
