from typing import *
import Mouse
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self,
                 offset: Tuple[Union[int, float], Union[int, float]],
                 icons: Tuple[pygame.Surface, ...],
                 callback: Callable[[], None]):
        super().__init__()
        self.x, self.y = 0, 0
        self.icons = (icons[0:2], icons[2:])  # (not full-screen: (normal, hovered), full-screen: (normal, hovered))
        self.image = self.icons[0][0]
        self.width, self.height = self.image.get_size()
        self.x_offset, self.y_offset = offset
        self.callback_func = callback
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def update_pos(self, screen_size: Tuple[Union[int, float], Union[int, float]]) -> None:
        self.x = screen_size[0] - self.x_offset
        self.y = screen_size[1] - self.y_offset
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_icon(self, hover: bool, full_screen: bool) -> None:
        self.image = self.icons[full_screen][hover]
        self.mask = pygame.mask.from_surface(self.image)

    def mouse_collide(self, mouse_obj: Mouse.Cursor, full_screen: bool) -> None:
        colliding = bool(pygame.sprite.collide_rect(self, mouse_obj))
        self.update_icon(colliding, full_screen)
        if colliding and mouse_obj.get_button_state(1):
            self.callback_func()

    def update(self,
               mouse_obj: Mouse.Cursor,
               screen_size: Tuple[Union[int, float], Union[int, float]],
               full_screen: bool) -> None:
        self.update_pos(screen_size)
        self.mouse_collide(mouse_obj, full_screen)


class ButtonGroup(pygame.sprite.GroupSingle):
    def __init__(self,
                 image_paths: Tuple[str, ...],
                 callback: Callable[[], None]):
        super().__init__()
        self.surfaces = tuple(pygame.image.load(path) for path in image_paths)
        self.callback = callback
        self.button = None

    def init_button(self, offset: Tuple[Union[int, float], Union[int, float]]) -> None:
        self.button = Button(offset, self.surfaces, self.callback)
        self.add(self.button)

    def get_icon_size(self) -> Tuple[int, int]:
        return self.surfaces[0].get_size()  # Both icons are the same size, so it doesn't matter which one we return.
