import Path
import Background
import Text
import Widgets
import Mouse
import pygame


class MainProc:
    def __init__(self):
        pygame.init()
        # region Monitor Info
        self.monitor_info = pygame.display.Info()
        self.monitor_res = (self.monitor_info.current_w, self.monitor_info.current_h)
        # endregion
        # region Game Data
        self.min_res = (480, 360)  # Stores the minimum window resolution allowed.
        self.current_res = self.min_res  # Stores the current size of the window.
        self.restore_res = self.min_res  # Stores the window size right before a switch to full-screen mode.
        self.fps = 60
        self.full_screen = False
        self.game_run = True
        # endregion
        # region Game Objects
        display_text = "you are an idiot\n☺ ☺ ☺"
        self.background = Background.Color()
        self.text_group = Text.TextGroup(tuple(display_text.split("\n")),
                                         Path.fix_path("./Fonts/Arial.ttf"),
                                         100,
                                         (40, 60))
        self.button_group = Widgets.ButtonGroup((Path.fix_path("./Images/UI Assets/Small Un-hovered.bmp"),
                                                 Path.fix_path("./Images/UI Assets/Small Hovered.bmp"),
                                                 Path.fix_path("./Images/UI Assets/Full Un-hovered.bmp"),
                                                 Path.fix_path("./Images/UI Assets/Full Hovered.bmp")),
                                                self.toggle_full_screen)
        button_size = self.button_group.get_icon_size()
        button_offset = (button_size[0] + 10, button_size[1] + 10)
        self.button_group.init_button(button_offset)
        self.mouse_object = Mouse.Cursor()
        # endregion
        # region Window Setup
        pygame.display.set_icon(pygame.image.load(Path.fix_path("./Images/Icon Resources/exe_icon.ico")))
        pygame.display.set_caption("You Are An Idiot")
        self.window = pygame.display.set_mode(self.current_res, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        # endregion
        while self.game_run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_run = False
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_object.update_pos(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Only left mouse button events need to be handled.
                    if event.button == 1:
                        self.mouse_object.set_button_state(1, True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_object.set_button_state(1, False)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.full_screen:
                            self.toggle_full_screen()
                elif event.type == pygame.VIDEORESIZE:  # Make sure to handle video resizing last.
                    if not self.full_screen:
                        self.current_res = (self.min_res[0] if event.w < self.min_res[0] else event.w,
                                            self.min_res[1] if event.h < self.min_res[1] else event.h)
                        self.window = pygame.display.set_mode(self.current_res,
                                                              pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            # region Game Logic
            self.background.update()
            self.text_group.update((self.current_res[0], self.current_res[1] - button_offset[1] - 10),
                                   self.background.get_state())
            self.button_group.update(self.mouse_object, self.current_res, self.full_screen)
            # endregion
            # region Screen Rendering
            self.window.fill(self.background.get_color())
            self.text_group.draw(self.window)
            self.button_group.draw(self.window)
            pygame.display.flip()
            # endregion

    def toggle_full_screen(self) -> None:
        if self.full_screen:
            self.current_res = self.restore_res
            self.window = pygame.display.set_mode(self.current_res,
                                                  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        else:
            self.restore_res = self.current_res
            self.current_res = self.monitor_res
            self.window = pygame.display.set_mode(self.current_res,
                                                  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self.full_screen = not self.full_screen


if __name__ == "__main__":
    MainProc()
