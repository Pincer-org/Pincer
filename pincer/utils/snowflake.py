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

    :var timestamp:
        Milliseconds since Discord Epoch,
        the first second of 2015 or 14200704000000

    :var worker_id:
        Internal worker ID

    :var process_id:
        Internal process ID

    :var increment:
        For every ID that is generated on that process,
        this number is incremented
    """

    @property
    def timestamp(self) -> int:
        return self >> 22

    @property
    def worker_id(self) -> int:
        return (self >> 17) % 16

    @property
    def process_id(self) -> int:
        return (self >> 12) % 16

    @property
    def increment(self) -> int:
        return self % 2048
