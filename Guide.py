import os
import pygame
from Cursor import Cursor
class Guide:
    def __init__(self, screen):
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")
        self.screen = screen
        self.font = pygame.font.Font(font_path, 60)
        self.background = pygame.transform.scale( pygame.image.load("data/Guide.png"),
                                                        (screen.get_width(), screen.get_height()) )
        self.color = (255, 255, 255)
        self.cursor = Cursor()
        self.cursor.changeType(2)
        self.back_text = self.font.render("Powrot", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(20, 20))
        game_makers_screen = True
        while game_makers_screen:
            screen.fill((19, 19, 19))
            screen.blit(self.background, self.background.get_rect())
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.back_rect.collidepoint(pygame.mouse.get_pos()):
                        game_makers_screen = False
            screen.blit(self.back_text, self.back_rect)
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
