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

from __future__ import annotations
from datetime import datetime
from typing import Optional, TypeVar, Union

DISCORD_EPOCH = 1420070400
TS = TypeVar("TS", str, datetime, float, int)


class Timestamp:
    """
    Contains a lot of useful methods for working with timestamps.
    """
    def __init__(self, time: Optional[TS] = None):
        self.__time = Timestamp.parse(time)
        self.__epoch = Timestamp.to_epoch(self.__time)
        self.date, self.time = str(self).split()

    @staticmethod
    def to_epoch(time: datetime) -> int:
        """
        Convert a datetime to an epoch.

        :param time:
            The datetime to convert.
        """
        return int(time.timestamp() * 1000)

    @staticmethod
    def string_to_datetime(string: str) -> datetime:
        """
        Convert a string to a datetime object.

        :param string:
            The string to convert.
        """
        return datetime.fromisoformat(string)

    @staticmethod
    def epoch_to_datetime(epoch: Union[int, float]) -> datetime:
        """
        Convert an epoch to a datetime object.

        :param epoch:
            The epoch to convert to a datetime object.
        """
        return datetime.utcfromtimestamp(epoch)

    @staticmethod
    def parse(time: Optional[TS] = None) -> datetime:
        """
        Convert a time to datetime object.

        :param time:
            The time to be converted to a datetime object.
            This can be one of these types: datetime, float, int, str

            If no parameter is passed it will return the current
            datetime.
        """
        if isinstance(time, datetime):
            return time

        elif isinstance(time, str):
            return Timestamp.string_to_datetime(time)

        elif isinstance(time, (int, float)):
            dt = Timestamp.epoch_to_datetime(t := int(time))

            if dt.year < 2015:  # if not Discord Epoch
                t += DISCORD_EPOCH  # make it Unix Epoch
            return Timestamp.epoch_to_datetime(t)

        return datetime.now()

    def __getattr__(self, key: str) -> int:
        return getattr(self.__time, key)

    def __str__(self) -> str:
        if len(string := str(self.__time)) == 19:
            return string + ".000"
        return string[:-3]

    def __int__(self) -> int:
        return self.__epoch  # in milliseconds

    def __float__(self) -> float:
        return self.__epoch / 1000  # in seconds

    def __ge__(self, other: Timestamp) -> bool:
        return self.__epoch >= other.__epoch

    def __gt__(self, other: Timestamp) -> bool:
        return self.__epoch > other.__epoch

    def __le__(self, other: Timestamp) -> bool:
        return self.__epoch <= other.__epoch

    def __lt__(self, other: Timestamp) -> bool:
        return self.__epoch < other.__epoch

    def __eq__(self, other: Timestamp) -> bool:
        return self.__epoch == other.__epoch

    def __ne__(self, other: Timestamp) -> bool:
        return self.__epoch != other.__epoch
