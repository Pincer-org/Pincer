# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

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
