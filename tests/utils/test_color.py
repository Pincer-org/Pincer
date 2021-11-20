from pincer.utils import Color


class TestSnowflake:

    def test_conversion(self):
        c = Color("aabbcc")
        assert c.r == 170
        assert c.g == 187
        assert c.b == 204
        assert c.hex == 'aabbcc'
