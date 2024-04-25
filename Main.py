import pygame
import os
import menu
from Cursor import Cursor
class Main:

    def __init__(self):
        pygame.init()

        # Ustawienia menu
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load("data/music/Gothic 1 Soundtrack  Swamp Camp  Ambient + Music.mp3")
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h
        self.main_menu = menu.Menu(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)

        # Ustawienie rozmiaru okna
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Gothic Gwint")

    def run(self):
        pygame.mixer.music.play()
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # LMB
                        mouse_pos = pygame.mouse.get_pos()
                        if self.main_menu.handle_click() == 3:
                            menu_running = False
            self.main_menu.draw(self.window)
            cursor = Cursor()
            cursor.update()
            cursor.draw(self.window)

            pygame.display.update()

        # Zamknięcie Pygame
        pygame.quit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()
