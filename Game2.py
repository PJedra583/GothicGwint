import os
import pygame
from Cursor import Cursor
class Game2:
    def __init__(self,screen,manager):
        running = True
        self.background_image = pygame.transform.scale(pygame.image.load("data/Plansza.jpg"),
                                                       (screen.get_width(), screen.get_height()))
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 70)
        self.cursor = Cursor()
        while running:
            for event in pygame.event.get():
                x = 5
            screen.blit(self.background_image, self.background_image.get_rect())
            self.cursor.update()
            self.cursor.draw(screen)
            pygame.display.update()


