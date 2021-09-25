# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from pincer.core.dispatch import GatewayDispatch


class TestDispatch:
    op = 123
    data = {
        "foo": "bar",
        "bar": "foo"
    }
    seq = 456
    event_name = "test_event"

    dispatch_string = (
        '{"op": 123, "d": {"foo": "bar", "bar": "foo"}, '
        '"s": 456, "t": "test_event"}'
    )

    dispatch = GatewayDispatch(op, data, seq, event_name)

    def test_string_fmt(self):
        """
        Tests whether or not the dispatch class its string conversion
        is correct.
        """
        assert str(self.dispatch) == self.dispatch_string

    def test_from_string(self):
        """
        Tests whether or not the from_string function is properly
        parsing the string and creating a GatewayDispatch instance.
        """
        assert (
            str(GatewayDispatch.from_string(self.dispatch_string))
            == self.dispatch_string
        )
