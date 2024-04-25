import pygame
import os
import menu

class Main:
    def __init__(self):
        pygame.init()

        # Ustawienia menu

        self.main_menu = menu.Menu()

        # Pobranie rozmiaru ekranu
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h

        # Ustawienie rozmiaru okna
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Gothic Gwint")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # LMB
                        mouse_pos = pygame.mouse.get_pos()
                        if self.main_menu.handle_click(mouse_pos):  #
                            running = False

            # Wyczyszczenie ekranu
            self.window.fill((255, 255, 255))

            # Rysowanie menu
            self.main_menu.draw(self.window)

            # Zaktualizowanie ekranu
            pygame.display.flip()

        # Zamknięcie Pygame
        pygame.quit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()
