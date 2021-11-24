# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from pincer.utils.conversion import remove_none


class TestSnowflake:

    def test_remove_none(self):
        assert remove_none([None, 1]) == [1]
        assert remove_none({None, 1}) == {1}
        assert remove_none({'a': 1, 'b': None}) == {'a': 1}
