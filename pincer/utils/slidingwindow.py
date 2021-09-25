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
from time import time


class SlidingWindow:

    def __init__(self, capacity: int, time_unit: float):
        self.capacity: int = capacity
        self.time_unit: float = time_unit

        self.__cur_time: float = time()
        self.__pre_count: int = capacity
        self.__cur_count: int = 0

    def allow(self) -> bool:
        # Reset rate limit:
        if (time() - self.__cur_time) > self.time_unit:
            self.__cur_time = time()
            self.__pre_count = self.__cur_count
            self.__cur_count = 0

        # Calculate the estimated count
        passed_time = time() - self.__cur_time
        time_cnt = (self.time_unit - passed_time) / self.time_unit
        est_cnt = self.__pre_count * time_cnt + self.__cur_count

        # Request has passed the capacity
        if est_cnt > self.capacity:
            return False

        self.__cur_count += 1
        return True
