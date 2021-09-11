# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
