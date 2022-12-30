from typing import *
from operator import itemgetter
import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (1, 1, 1)


class Text(pygame.sprite.Sprite):
    def __init__(self,
                 text_lines: Tuple[str],
                 font_object: pygame.font.Font,
                 padding: Tuple[Union[int, float], Union[int, float]]):
        super().__init__()
        self.prev_invert = False
        self.text_lines = text_lines
        self.font = font_object
        self.x, self.y = 0, 0
        self.h_pad, self.v_pad = padding
        get_width = itemgetter(0)
        get_height = itemgetter(1)
        self.line_sizes = tuple(self.font.size(line) for line in text_lines)
        self.text_width = max(self.line_sizes, key=get_width)[0] + self.h_pad  # Get the width of the widest line.
        self.text_height = sum(get_height(size) for size in self.line_sizes) + self.v_pad  # Get sum of text height.
        self.current_width = self.text_width
        self.current_height = self.text_height
        self.hw_ratio = self.text_height / self.text_width  # hw_ratio = height:width
        self.original_surf = pygame.Surface((self.text_width, self.text_height))
        # This surface will be rendered more often than it is modified, so use the accelerated blit flag.
        self.original_surf.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
        self.render_text(WHITE)
        self.image = self.original_surf.copy()
        self.rect = pygame.Rect(self.x, self.y, self.text_width, self.text_height)

    def render_text(self, color: Tuple[int, int, int]) -> None:
        self.original_surf.fill(TRANSPARENT)
        accumulated_y = self.v_pad / 2
        for index, text in enumerate(self.text_lines):
            x = self.text_width / 2 - self.line_sizes[index][0] / 2
            self.original_surf.blit(self.font.render(self.text_lines[index], True, color), (x, accumulated_y))
            accumulated_y += self.line_sizes[index][1]

    def resize_surf(self, bounds: Tuple[int, int]) -> None:
        """
        Resizes surface to fit bounds.
        """
        # Scale to height if scaling to the boundary's width makes the object too high, else scale to width.
        if bounds[0] * self.hw_ratio > bounds[1]:
            new_height = bounds[1]
            new_width = new_height / self.hw_ratio
        else:
            new_width = bounds[0]
            new_height = new_width * self.hw_ratio
        self.current_width, self.current_height = new_width, new_height
        self.image = pygame.transform.scale(self.original_surf, (self.current_width, self.current_height))

    def update_pos(self, area_size: Tuple[int, int]) -> None:
        """
        Centers the surface in the middle of the rendering area. Make sure to resize the surface first before calling
        this method.
        """
        if self.current_width < area_size[0]:
            self.x = area_size[0] / 2 - self.current_width / 2
            self.y = 0
        else:
            self.x = 0
            self.y = area_size[1] / 2 - self.current_height / 2
        self.rect = pygame.Rect(self.x, self.y, self.current_width, self.current_height)

    def update(self, area_size: Tuple[int, int], invert: bool) -> None:
        if self.prev_invert is not invert:
            self.prev_invert = invert
            self.render_text(BLACK if invert else WHITE)
        self.resize_surf(area_size)  # Updates surface
        self.update_pos(area_size)  # Updates position


class TextGroup(pygame.sprite.GroupSingle):
    def __init__(self,
                 text_lines: Tuple[str],
                 font_path: str,
                 font_size: int,
                 padding: Tuple[Union[int, float], Union[int, float]]):
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)  # Larger font size results in clearer font graphics.
        self.text_object = Text(text_lines, self.font, padding)
        self.add(self.text_object)
