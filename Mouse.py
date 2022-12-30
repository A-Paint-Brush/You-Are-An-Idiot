from typing import *
import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.buttons = [False]
        self.x, self.y = 0, 0
        self.width, self.height = 1, 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.Mask((1, 1), fill=True)  # Hit-box of the mouse cursor is exactly 1 pixel.

    def update_pos(self, new_pos: Tuple[int, int]) -> None:
        self.x, self.y = new_pos
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_pos(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_button_state(self, button_number: int, state: bool) -> None:
        self.buttons[button_number - 1] = state

    def get_button_state(self, button_number: int) -> bool:
        return self.buttons[button_number - 1]
