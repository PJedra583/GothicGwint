import pygame
import os
class Menu:

    def __init__(self,width,height):
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 70)
        self.color = (255, 255, 255)
        self.items = ["Rozpocznij gre", "Samouczek", "Tworcy gry", "Exit"]
        self.background_image = pygame.transform.scale( pygame.image.load("data/Background4.jpg"),(width,height) )
        self.background_rect = self.background_image.get_rect()
        self.rects = []
        self.texts = []

    def draw(self, screen):
        screen.blit(self.background_image, self.background_rect)

        menu_height = len(self.items) * 80
        y = (screen.get_height() - menu_height) // 2  # Begin position for Y
        for item in self.items:
            text = self.font.render(item, True, self.color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, y))
            self.texts.append(text)
            self.rects.append(text_rect)
            screen.blit(text, text_rect)
            y += 80

    def handle_click(self):
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
             return self.rects.index(rect)
        return -1

    def handle_hover(self):
        pass


