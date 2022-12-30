from typing import *
from math import *
import Time


class Color:
    def __init__(self):
        self.invert = False
        self.delay = 0.4
        self.timer = Time.Timer()
        self.timer.reset_timer()

    def update(self) -> None:
        time = self.timer.get_time()
        if time >= self.delay:
            delta_time = time - self.delay
            compensation = divmod(delta_time, self.delay)
            for i in range(floor(compensation[0]) + 1):
                self.invert = not self.invert
            self.timer.force_elapsed_time(compensation[1])

    def get_color(self) -> Tuple[int, int, int]:
        return (255 * self.invert,) * 3

    def get_state(self) -> bool:
        return self.invert
