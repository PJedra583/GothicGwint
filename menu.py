import pygame
import os
from Cursor import Cursor

class Menu:

    def __init__(self,screen):
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 70)
        self.color = (255, 255, 255)
        self.items = ["Rozpocznij gre", "Samouczek", "Tworcy gry", "Exit"]
        self.background_image = pygame.transform.scale( pygame.image.load("data/Background4.jpg"),
                                                        (screen.get_width(), screen.get_height()) )
        self.background_rect = self.background_image.get_rect()
        self.rects = []
        self.texts = []
        self.cursor = Cursor()
        self.hover_sound = pygame.mixer.Sound("data/sound/hover.mp3")
        self.lock = False
        menu_height = len(self.items) * 80
        y = (screen.get_height() - menu_height) // 2  # Begin position for Y
        for item in self.items:
            text = self.font.render(item, True, self.color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, y))
            self.texts.append(text)
            self.rects.append(text_rect)
            y += 80
    def draw(self, screen):

        screen.blit(self.background_image, self.background_rect)
        for i in range(len(self.rects)):
            screen.blit(self.texts[i], self.rects[i])
        self.cursor.update()
        self.cursor.draw(screen)



    def handle_click(self):
        for i in range(len(self.rects)):
            if self.rects[i].collidepoint(pygame.mouse.get_pos()):
             return i
        return -1

    def handle_hover(self):
        #lock do zarządzania czy kursor ruszył się z pola tekstowego
        #opcjonalnie jeżeli i != poprzednie i to zastopowac dzwiek i zagrac ponownie
        was_cursor_on_text = False
        for i in range(len(self.rects)):
            if self.rects[i].collidepoint(pygame.mouse.get_pos()):
                self.texts[i] = self.font.render(self.items[i], True, (19,19,19))
                if not self.lock :
                 self.hover_sound.play()
                 self.lock = True
                was_cursor_on_text = True
            else:
                self.texts[i] = self.font.render(self.items[i], True, self.color)
        if was_cursor_on_text :
            self.cursor.changeType(1)
        else:
            self.cursor.changeType(2)
            self.lock = False




