from pincer.utils import Color


class TestSnowflake:

    def test_conversion(self):
        c = Color("#aabb01")
        assert c.r == 170
        assert c.g == 187
        assert c.b == 1
        assert c.hex == 'aabb01'
