import pygame
import os
from Cursor import Cursor
class PlayerScreen:
    def __init__(self,screen):
        self.background_image = pygame.transform.scale(pygame.image.load("data/connect.jpg"),
                                                       (screen.get_width(), screen.get_height()))
        self.background_rect = self.background_image.get_rect()
        self.font_gothic = pygame.font.Font(os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf"), 36)
        self.font = pygame.font.Font(None, 26)
        self.cursor = Cursor()
        self.cursor.changeType(2)

        self.back_text = self.font_gothic.render("Wroc", True, "BLack")
        self.connect_text = self.font_gothic.render("Polacz", True, "BLack")

        self.back_text_rect = self.back_text.get_rect(
            topleft=(screen.get_width() // 2.5 + 30, screen.get_height() // 4 + 350))
        self.connect_text_rect = self.connect_text.get_rect(
            topleft=(screen.get_width() // 2.5 + 200, screen.get_height() // 4 + 350))

        running = True
        input_text = ""
        while running:
            screen.fill((255,255,255))
            screen.blit(self.background_image,self.background_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 and self.back_text_rect.collidepoint(pygame.mouse.get_pos()):
                        running = False
                    elif event.button == 1 and self.connect_text_rect.collidepoint(pygame.mouse.get_pos()):
                        input_text = ""



            #Kolejnosc rysowania istotna
            pygame.draw.rect(screen,(217,186,140),(screen.get_width() //2.5  ,
                                                   screen.get_height() //4 ,300,400))
            pygame.draw.rect(screen,"Gold",(screen.get_width() //2.5  ,screen.get_height() //4 ,300,400),
                             10)


            text_surface = self.font_gothic.render("Podaj adres IP", True, "Black")
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
            screen.blit(text_surface, text_rect)


            text_surface = self.font.render(input_text, True, "BLack")
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2.5))
            screen.blit(text_surface, text_rect)



            screen.blit(self.back_text,self.back_text_rect)
            screen.blit(self.connect_text,self.connect_text_rect)


            self.cursor.update()
            self.cursor.draw(screen)

            self.handle_hover()


            pygame.display.update()

    def handle_hover(self):

        was_cursor_on_text = False
        if self.back_text_rect.collidepoint(pygame.mouse.get_pos()):
            self.back_text = self.font_gothic.render("Wroc", True, "green")
            was_cursor_on_text = True
        else:
            self.back_text = self.font_gothic.render("Wroc", True, "black")

        if self.connect_text_rect.collidepoint(pygame.mouse.get_pos()):
            self.connect_text = self.font_gothic.render("Polacz", True, "green")
            was_cursor_on_text = True
        else:
            self.connect_text = self.font_gothic.render("Polacz", True, "black")

        if was_cursor_on_text:
            self.cursor.changeType(1)
        else:
            self.cursor.changeType(2)