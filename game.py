import os
import pygame
from Cursor import Cursor
from Card import Card
CARD_SIZE_X = 75
CARD_SIZE_Y = 100
class Game:

    def __init__(self,screen):

        self.screen = screen
        self.background_image = pygame.transform.scale(pygame.image.load("data/Plansza.jpg"),
                                                       (screen.get_width(), screen.get_height()))
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 70)
        self.my_cards = []
        self.opponent_cards = []
        self.my_score = 10
        self.opponent_score = 0
        self.cursor = Cursor()
        self.heroCard = None
        self.hp = 2
        self.falling_text_x = 0
        self.turn = True

    def run(self):

        c = Card(None,None,None,None)
        c.load_cards()
        for i in range(10):
            self.my_cards.append(c.getCard())
        self.heroCard = c.getHeroCard()

        running = True
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        while running:
            for event in pygame.event.get():
                x = 5
            self.screen.blit(self.background_image, self.background_image.get_rect())
            self.cursor.update()
            self.cursor.draw(self.screen)

            #Linia statystyk, karta bohatera gora,pasek wyniku przeciwnik, pasek wyniku gracz
            #karta bohatera dol,kolo gora, kolo dol
            pygame.draw.line(self.screen, "black", (screen_width * 0.2, 0),
                             (screen_width * 0.2, screen_height), 9)

            #Statystyki

            #Karty bohaterow
            pygame.draw.rect(self.screen, "black", (screen_width * 0.025, screen_height * 0.025,
                                                    CARD_SIZE_X, CARD_SIZE_Y))

            pygame.draw.rect(self.screen, "black", (screen_width * 0.025, screen_height * 0.80,
                                                    CARD_SIZE_X, CARD_SIZE_Y))

            hero = pygame.transform.scale(self.heroCard.image, (CARD_SIZE_X, CARD_SIZE_Y))
            self.screen.blit(hero, (screen_width * 0.025, screen_height * 0.80,
                                    CARD_SIZE_X, CARD_SIZE_Y))

            # Prostokat

            pygame.draw.rect(self.screen, "black", (0, screen_height // 4, screen_width * 0.2, screen_height * 0.2))

            pygame.draw.rect(self.screen, "black", (0, screen_height - (screen_height // 4) - screen_height * 0.2,
                                        screen_width * 0.2, screen_height * 0.2)) #bo rect.height = screen.height * 0.2

            #Zycia
            image = pygame.image.load("data/HP.jpg")
            image = pygame.transform.scale(image, (50, 50))
            self.screen.blit(image, (0+screen_width*0.08, screen_height - (screen_height // 4)-(screen_height * 0.075) ))
            self.screen.blit(image, (0+screen_width*0.12, screen_height - (screen_height // 4)-(screen_height * 0.075) ))

            self.screen.blit(image,(0+screen_width*0.08, screen_height // 4+(screen_height * 0.125) ))
            self.screen.blit(image,(0+screen_width*0.12, screen_height // 4+(screen_height * 0.125) ))


            #linie
            space_for_line = SCREEN_HEIGHT//8
            for i in range(1, 8):
                pygame.draw.line(self.screen,"black",(screen_width*0.25,space_for_line*i ),
                                 (screen_width, space_for_line*i),2)

            pygame.draw.line(self.screen, "black", (screen_width * 0.25, 0),
                                 (screen_width * 0.25, screen_height), 5)
            pygame.draw.line(self.screen, "black", (screen_width * 0.35, space_for_line),
                             (screen_width * 0.35, screen_height-space_for_line), 5)

            # kola wynikow
            pygame.draw.circle(self.screen, "white",
                               (screen_width * 0.2, screen_height // 4 + (screen_height * 0.1))
                               , 30)
            pygame.draw.circle(self.screen, "white", (screen_width * 0.2, screen_height - (screen_height // 4) -
                                                      (screen_height * 0.1)), 30)

            text_surface = self.font.render(str(self.my_score), True, "Black")
            text_rect = text_surface.get_rect(center=(screen_width * 0.2, screen_height // 4 + (screen_height * 0.1)))
            self.screen.blit(text_surface, text_rect)

            text_surface = self.font.render(str(self.my_score), True, "Black")
            text_rect = text_surface.get_rect(center=(screen_width * 0.2, screen_height - (screen_height // 4) -
                                                      (screen_height * 0.1)))
            self.screen.blit(text_surface, text_rect)

            #karty
            for i in range(len(self.my_cards)) :
                scaled_image = pygame.transform.scale(self.my_cards[i].image, (CARD_SIZE_X, CARD_SIZE_Y))
                self.screen.blit(scaled_image, (screen_width * 0.26+(i*CARD_SIZE_X*0.9), screen_height-CARD_SIZE_Y))

            handle_hover(self,self.screen)
            falling_text(self,self.screen)
            pygame.display.update()


def handle_hover(self, screen):
    mouse_pos = pygame.mouse.get_pos()
    i = 0;
    for card in self.my_cards:
        card_rect = pygame.Rect((screen.get_width() * 0.26+(i*CARD_SIZE_X*0.9), screen.get_height() - CARD_SIZE_Y), (CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, (screen.get_width() // 2.5, screen.get_height() // 2.5))
        i+=1

def falling_text(self,screen):
    text_surface = self.font.render("Twoj Ruch", True, "Red")
    text_rect = text_surface.get_rect(center=(self.falling_text_x, screen.get_height()//2))
    if self.falling_text_x >= screen.get_width()//2 and self.turn:
        self.turn = False
        pygame.time.delay(2000)
    self.falling_text_x += 10
    self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main_instance = Game(window)
    main_instance.run()


