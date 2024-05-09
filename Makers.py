import pygame
import os
from Cursor import Cursor


class Makers:
    def __init__(self, screen):
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")
        font_path_comic = os.path.join("data", "fonts", "comic.ttf")
        self.screen = screen
        self.font = pygame.font.Font(font_path, 60)
        self.color = (255, 255, 255)
        self.cursor = Cursor()
        self.cursor.changeType(2)
        self.back_text = self.font.render("Powrot", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(20, 20))

        self.makers_items = \
            ["Oprogramowanie: Piotr Jędra","Udźwiękowienie: Franciszek Kalinowski","Karty do gry: Quash"]
        self.makers_names = pygame.font.Font(font_path_comic, 40)
        self.makers_y = -300 # Początkowa pozycja dla pierwszego tekstu
        game_makers_screen = True
        while game_makers_screen:
            screen.fill((19, 19, 19))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.back_rect.collidepoint(pygame.mouse.get_pos()):
                        game_makers_screen = False
            screen.blit(self.back_text, self.back_rect)
            self.falling_text(screen)
            if (self.makers_y >= screen.get_height()+300 ) :
                self.makers_y = -300
            else: self.makers_y += 1
            self.handle_hover()
            self.cursor.update()
            self.cursor.draw(screen)
            pygame.display.update()


    def handle_hover(self):

        was_cursor_on_text = False
        if self.back_rect.collidepoint(pygame.mouse.get_pos()):
            self.back_text = self.font.render("Powrot", True, "green")
            was_cursor_on_text = True
        else:
            self.back_text = self.font.render("Powrot", True, self.color)
        if was_cursor_on_text :
            self.cursor.changeType(1)
        else:
            self.cursor.changeType(2)

    def falling_text(self, screen):
        text_gap = 100
        y_offset = self.makers_y

        for name in self.makers_items:
            text_surface = self.makers_names.render(name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midtop=(self.screen.get_width() // 2, y_offset))
            y_offset += text_gap  # Przesunięcie pionowe dla kolejnego tekstu

            screen.blit(text_surface, text_rect)
