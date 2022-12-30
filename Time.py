from typing import *
import pygame


class Timer:
    def __init__(self):
        self.current_time = None

    def reset_timer(self) -> None:
        self.current_time = pygame.time.get_ticks() / 1000

    def get_time(self) -> float:
        return 0.0 if self.current_time is None else pygame.time.get_ticks() / 1000 - self.current_time

    def force_elapsed_time(self, value: Union[int, float]) -> None:
        self.current_time = pygame.time.get_ticks() / 1000 - value
