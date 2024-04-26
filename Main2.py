import pygame
import menu

import ConnectionManager
from Makers import Makers
from PlayerScreen1 import PlayerScreen
from PlayerScreen2 import PlayerScreen2
class Main:

    def __init__(self):
        pygame.init()

        # Ustawienia menu
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load("data/music/Gothic 1 Soundtrack  Swamp Camp  Ambient + Music.mp3")
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.main_menu = menu.Menu(self.window)

        # Ustawienie rozmiaru okna
        pygame.display.set_caption("Gothic Gwint")

    def run(self):
      #  pygame.mixer.music.play()
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # LMB
                        button_number = self.main_menu.handle_click()
                        #Stworz,Dolacz,Samouczek,tworcy,exit
                        if button_number == 0:
                            PlayerScreen(self.window)
                        elif button_number == 1:
                            PlayerScreen2(self.window)
                        elif button_number == 2:
                            print()
                        elif button_number == 3:
                            Makers(self.window)
                        elif button_number == 4:
                            menu_running = False
            self.main_menu.draw(self.window)
            self.main_menu.handle_hover()
            pygame.display.update()

        # Zamknięcie Pygame
        pygame.quit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()
