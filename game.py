import os
import threading

import pygame
import socket

import ConnectionManager

from GraphicEffects import GraphicEffects
from Cursor import Cursor
from Card import Card
CARD_SIZE_X = 75
CARD_SIZE_Y = 100

class Game:

    def __init__(self,screen,server_ip,player):

        self.server_ip = server_ip
        self.screen = screen
        self.player = player

        self.c = Card.getInstance()
        if player == 1 :
            self.c.load_cards()
        self.all_Cards = Card.getSortedDeck()
        self.allHeroes = Card.getHeroes()

        self.background_image = pygame.transform.scale(pygame.image.load("data/Plansza.jpg"),
                                                       (screen.get_width(), screen.get_height()))
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 70)
        self.font_comic = pygame.font.Font(os.path.join("data", "fonts", "comic.ttf"), 100)
        self.my_cards = []
        self.opponent_cards_len = 0
        self.my_score = 0
        self.opp_score = 0
        self.cursor = Cursor()
        self.heroCard = None
        self.opp_heroCard = None
        self.hp = 2
        self.opp_hp = 2
        self.falling_text_x = 0
        self.turn = None
        self.choosing = False
        self.pos_in_choose = 0
        self.cards_in_choose = []
        self.clock = pygame.time.Clock()
        self.timer = 0
        self.messageClock = pygame.time.Clock()
        self.messageTimer = 0
        self.cardReverse = pygame.transform.scale(pygame.image.load("data/textures/rewers.jpg"),(CARD_SIZE_X,CARD_SIZE_Y))
        self.cardToAttack = pygame.transform.scale(pygame.image.load("data/textures/In Extremo.jpg"),(CARD_SIZE_X,CARD_SIZE_Y))
        self.player_num = player
        self.stopHover = False
        self.rects_to_display = []
        self.card_to_display = None
        self.hero_card_to_display = None
        self.moved = False

        self.passed = False
        self.oppPassed = False
        #Pole bitwy
        self.MyFrontRow = []
        self.MyMiddleRow = []
        self.MyBackRow = []

        self.OppFrontRow = []
        self.OppMiddleRow = []
        self.OppBackRow = []

        self.myScores = None
        self.oppScores = None

        self.isHeroActive = None
        self.isOppHeroActive = None


        self.weather = "FFF"
        self.toAttack = None
        self.oppToAttack = None

        #polaczenie z serwerem
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, 8091))

        #efekty
        self.graphicEffects = GraphicEffects(screen)
        self.graphicEffectsOpp = GraphicEffects(screen)

        space_for_line = self.screen.get_height() // 8
        rain_area = (int(screen.get_width() * 0.25), int(space_for_line * 6), int(screen.get_width()),
                     int(space_for_line * 6)+int(space_for_line))
        rain_area_opp = (int(screen.get_width() * 0.25), int(space_for_line * 1), int(screen.get_width()),
                     int(space_for_line * 1) + int(space_for_line))
        self.graphicEffects.make_rain(rain_area,250)
        self.graphicEffectsOpp.make_rain(rain_area_opp, 250)

        snow_area = (int(screen.get_width() * 0.25),int(space_for_line*3),int(screen.get_width()),
                                                                int(space_for_line*3)+int(2*space_for_line))
        self.graphicEffects.make_snow(snow_area,250)
        fog_area = (int(screen.get_width() * 0.25), int(space_for_line * 5), int(screen.get_width()),
                     int(space_for_line * 5)+int(space_for_line))
        fog_area_opp = (int(screen.get_width() * 0.25), int(space_for_line * 2), int(screen.get_width()),
                     int(space_for_line * 2)+int(space_for_line))
        self.graphicEffects.make_fog(fog_area,100)
        self.graphicEffectsOpp.make_fog(fog_area_opp,100)

        self.endGame = False
        self.endGameText=''
        self.endGameClock=pygame.time.Clock()
        self.endGameTimer=0

    def run(self):

       prepare_battlefield(self)
       running = True
       screen_width = self.screen.get_width()
       screen_height = self.screen.get_height()

       while running:
            if self.moved:
                if self.turn:
                 prepare_battlefield(self)
                else:
                 prepare_battlefield(self)
                 #ponieważ nie wiemy czy oponent się ruszył
                 if self.passed:
                   self.moved = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.stopHover = False
                    if event.button == 1:  # LMB
                        if self.turn :
                         checkIfMove(self)
                         self.rects_to_display = []
                         self.card_to_display = None
                         self.hero_card_to_display = None
                         handle_click(self,self.screen)
                    #dla innych przycików myszy
                    else:
                        self.rects_to_display = []
                        self.card_to_display = None
                        self.hero_card_to_display = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.pos_in_choose+=1
                    elif event.key == pygame.K_LEFT:
                        self.pos_in_choose-=1
                    elif event.key == pygame.K_RETURN:
                        if self.choosing:
                            cardType = self.cards_in_choose[self.pos_in_choose].type
                            pos = 'w'
                            if cardType == "front" or cardType == "mixed":
                                pos = "f"
                            if cardType == "middle":
                                pos = "m"
                            if cardType == "back":
                                pos = "b"
                            mess = send_mess(self, "M;" + str(self.cards_in_choose[self.pos_in_choose].id) + ";" + pos + ";\n")
                            if mess.strip() == "Waiting":
                                send_mess(self, "E" + ";\n")
                            self.choosing = False
                            self.cards_in_choose = []
                            self.moved = True
                    elif event.key == pygame.K_SPACE:
                        if self.turn:
                            send_mess(self,"Pass\n")
                            self.turn = False
                            self.moved = True
            self.screen.blit(self.background_image, self.background_image.get_rect())


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

            hero = pygame.transform.scale(self.opp_heroCard.image, (CARD_SIZE_X, CARD_SIZE_Y))
            self.screen.blit(hero, (screen_width * 0.025, screen_height * 0.025,
                                    CARD_SIZE_X, CARD_SIZE_Y))
            color = "white"
            if self.isOppHeroActive.strip() == 'F':
                color = "red"
            pygame.draw.circle(self.screen,color,(screen_width * 0.025+CARD_SIZE_X+50,screen_height * 0.025+
                                                  (CARD_SIZE_Y//2)),12)
            color = "white"
            if self.isHeroActive.strip() == 'F':
                color = "red"
            pygame.draw.circle(self.screen, color, (screen_width * 0.025 + CARD_SIZE_X + 50, screen_height * 0.8 +
                                                    (CARD_SIZE_Y // 2)), 12)

            # Prostokat wyników
            pygame.draw.rect(self.screen, "black", (0, screen_height // 4, screen_width * 0.2, screen_height * 0.2))

            pygame.draw.rect(self.screen, "black", (0, screen_height - (screen_height // 4) - screen_height * 0.2,
                                        screen_width * 0.2, screen_height * 0.2)) #bo rect.height = screen.height * 0.2

            text_surface = self.font.render("Przeciwnik",True,"white")
            text_rect = text_surface.get_rect(center=(screen_width*0.1,(screen_height//4)+(screen_height*0.1)))
            self.screen.blit(text_surface,text_rect)

            text_surface = self.font.render("Ty", True, "white")
            text_rect = text_surface.get_rect(center=(screen_width * 0.1,
                                                      screen_height - (screen_height // 4) - (screen_height * 0.1)))
            self.screen.blit(text_surface, text_rect)

            #Zycia
            image = pygame.image.load("data/HP.jpg")
            image2 = pygame.image.load("data/EmptyHP.png")

            image = pygame.transform.scale(image, (50, 50))
            image2 = pygame.transform.scale(image2, (50, 50))

            if self.hp > 1 :
             self.screen.blit(image, (0+screen_width*0.08, screen_height - (screen_height // 4)-(screen_height * 0.075) ))
             self.screen.blit(image, (0+screen_width*0.12, screen_height - (screen_height // 4)-(screen_height * 0.075) ))
            elif self.hp > 0 :
             self.screen.blit(image, (0 + screen_width * 0.08, screen_height - (screen_height // 4) - (screen_height * 0.075)))
             self.screen.blit(image2, (0 + screen_width * 0.12, screen_height - (screen_height // 4) - (screen_height * 0.075)))
            else:
             self.screen.blit(image2, (0 + screen_width * 0.08, screen_height - (screen_height // 4) - (screen_height * 0.075)))
             self.screen.blit(image2, (0 + screen_width * 0.12, screen_height - (screen_height // 4) - (screen_height * 0.075)))

            if self.opp_hp > 1:
                 self.screen.blit(image, (0 + screen_width * 0.08, screen_height // 4 + (screen_height * 0.125)))
                 self.screen.blit(image, (0 + screen_width * 0.12, screen_height // 4 + (screen_height * 0.125)))
            elif self.opp_hp > 0:
                 self.screen.blit(image, (0 + screen_width * 0.08, screen_height // 4 + (screen_height * 0.125)))
                 self.screen.blit(image2, (0 + screen_width * 0.12, screen_height // 4 + (screen_height * 0.125)))
            else:
                 self.screen.blit(image2, (0 + screen_width * 0.08, screen_height // 4 + (screen_height * 0.125)))
                 self.screen.blit(image2, (0 + screen_width * 0.12, screen_height // 4 + (screen_height * 0.125)))

            #linie
            space_for_line = self.screen.get_height()//8
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
            if self.oppPassed :
                text_surface = self.font.render("PAS!", True, "Red")
                text_rect = text_surface.get_rect(
                    center=(screen_width * 0.2, screen_height // 4 + (screen_height * 0.1) + 50))
                self.screen.blit(text_surface, text_rect)

            pygame.draw.circle(self.screen, "white", (screen_width * 0.2, screen_height - (screen_height // 4) -
                                                      (screen_height * 0.1)), 30)
            if self.passed :
                text_surface = self.font.render("PAS!", True, "red")
                text_rect = text_surface.get_rect(
                    center=(screen_width * 0.2, screen_height - (screen_height // 4) -
                                                      (screen_height * 0.1)-50))
                self.screen.blit(text_surface, text_rect)
            text_surface = self.font.render(str(self.opp_score), True, "Black")
            text_rect = text_surface.get_rect(center=(screen_width * 0.2, screen_height // 4 + (screen_height * 0.1)))
            self.screen.blit(text_surface, text_rect)

            text_surface = self.font.render(str(self.my_score), True, "Black")
            text_rect = text_surface.get_rect(center=(screen_width * 0.2, screen_height - (screen_height // 4) -
                                                      (screen_height * 0.1)))
            self.screen.blit(text_surface, text_rect)

            #wyniki linie
            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height-
                                                      (space_for_line*2)+space_for_line//2), 30)
            text_surface = self.font.render(self.myScores.split(";")[2], True, "red")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height-
                                                      (space_for_line*2)+space_for_line//2))
            self.screen.blit(text_surface, text_rect)


            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height -
                                                      (space_for_line * 3) + space_for_line // 2), 30)
            text_surface = self.font.render(self.myScores.split(";")[1], True, "green")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height -
                                                      (space_for_line * 3) + space_for_line // 2))
            self.screen.blit(text_surface, text_rect)


            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height -
                                                      (space_for_line * 4) + space_for_line // 2), 30)
            text_surface = self.font.render(self.myScores.split(";")[0], True, "Blue")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height -
                                                      (space_for_line * 4) + space_for_line // 2))
            self.screen.blit(text_surface, text_rect)

            #=====================================

            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height -
                                                      (space_for_line * 5) + space_for_line // 2), 30)
            text_surface = self.font.render(self.oppScores.split(";")[0], True, "Blue")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height -
                                                      (space_for_line * 5) + space_for_line // 2))
            self.screen.blit(text_surface, text_rect)

            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height -
                                                      (space_for_line * 6) + space_for_line // 2), 30)
            text_surface = self.font.render(self.oppScores.split(";")[1], True, "red")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height -
                                                      (space_for_line * 6) + space_for_line // 2))
            self.screen.blit(text_surface, text_rect)


            pygame.draw.circle(self.screen, "white", (screen_width * 0.26, screen_height -
                                                      (space_for_line * 7) + space_for_line // 2), 30)
            text_surface = self.font.render(self.oppScores.split(";")[2], True, "green")
            text_rect = text_surface.get_rect(center=(screen_width * 0.26, screen_height -
                                                      (space_for_line * 7) + space_for_line // 2))
            self.screen.blit(text_surface, text_rect)

            #karty
            for i in range(len(self.my_cards)) :
                scaled_image = pygame.transform.scale(self.my_cards[i].image, (CARD_SIZE_X, CARD_SIZE_Y))
                self.screen.blit(scaled_image, (screen_width * 0.26+(i*CARD_SIZE_X*0.9), screen_height-CARD_SIZE_Y))

            for i in range(self.opponent_cards_len) :
                self.screen.blit(self.cardReverse, (screen_width * 0.26+(i*CARD_SIZE_X*0.9), 0))

            #pole bitwy
            for i in range(len(self.MyFrontRow)) :
                image = self.MyFrontRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*4) + (space_for_line-CARD_SIZE_Y)))
            for i in range(len(self.MyMiddleRow)) :
                image = self.MyMiddleRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*5) + (space_for_line-CARD_SIZE_Y)))
            for i in range(len(self.MyBackRow)) :
                image = self.MyBackRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*6) + (space_for_line-CARD_SIZE_Y)))
            #================
            for i in range(len(self.OppFrontRow)) :
                image = self.OppFrontRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*3) + (space_for_line-CARD_SIZE_Y)))
            for i in range(len(self.OppMiddleRow)) :
                image = self.OppMiddleRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*2) + (space_for_line-CARD_SIZE_Y)))
            for i in range(len(self.OppBackRow)) :
                image = self.OppBackRow[i].image
                image = pygame.transform.scale(image,(CARD_SIZE_X,CARD_SIZE_Y))
                self.screen.blit(image, (screen_width * 0.36+(i*CARD_SIZE_X*0.9),
                                                    (space_for_line*1) + (space_for_line-CARD_SIZE_Y)))

            #Rogi dowódcy
            if int(self.toAttack[0]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*4,CARD_SIZE_X,CARD_SIZE_Y))
            if int(self.toAttack[1]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*5,CARD_SIZE_X,CARD_SIZE_Y))
            if int(self.toAttack[2]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*6,CARD_SIZE_X,CARD_SIZE_Y))

            if int(self.oppToAttack[0]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*3,CARD_SIZE_X,CARD_SIZE_Y))
            if int(self.oppToAttack[1]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*2,CARD_SIZE_X,CARD_SIZE_Y))
            if int(self.oppToAttack[2]) > 1:
                self.screen.blit(self.cardToAttack, ((screen_width * 0.26)+60,space_for_line*1,CARD_SIZE_X,CARD_SIZE_Y))


            #pogoda
            if self.weather[0] == 'T':
                self.graphicEffects.draw_snow()
            if self.weather[1] == 'T':
                self.graphicEffects.draw_fog()
                self.graphicEffectsOpp.draw_fog()
            if self.weather[2] == 'T':
                self.graphicEffects.draw_rain()
                self.graphicEffectsOpp.draw_rain()

                # Ekran wyboru
                if self.choosing:
                    if len(self.cards_in_choose) == 0:
                        send_mess(self, "E" + ";\n")
                        self.choosing = False
                        self.moved = True
                        self.cards_in_choose = []
                    else:
                        if self.pos_in_choose < 0:
                            self.pos_in_choose = len(self.cards_in_choose) - 1
                        if self.pos_in_choose >= len(self.cards_in_choose):
                            self.pos_in_choose = 0
                        c = self.cards_in_choose[self.pos_in_choose]
                        self.screen.blit(c.image, c.image.get_rect(center=(self.screen.get_width() // 2,
                                                                           self.screen.get_height() // 2)))

            #wybor pola
            if not self.stopHover :
                handle_hover(self, self.screen)
            else:
                card_display_place = (self.screen.get_width() - 220, self.screen.get_height() // 2)
                if self.card_to_display is not None:
                    for rect in self.rects_to_display:
                        surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
                        pygame.draw.rect(surface, (255, 255, 0, 100), surface.get_rect())
                        self.screen.blit(surface, (rect[0], rect[1]))
                    self.screen.blit(self.all_Cards[self.card_to_display].image, card_display_place)
                elif self.hero_card_to_display is not None:
                    self.screen.blit(self.allHeroes[self.hero_card_to_display].image, card_display_place)

            falling_text(self, self.screen)
            self.cursor.update()
            self.cursor.draw(self.screen)
            if not self.endGame:
                if not self.turn:
                    if self.messageTimer >= 1:
                        s = send_mess(self, "GetMyTurn\n")
                        self.messageTimer = 0
                        self.messageClock = pygame.time.Clock()
                        if int(s) == 1:
                            self.turn = True
                            self.moved = True
                    self.messageTimer += self.messageClock.tick(60) / 1000
            else:
                if self.endGameTimer == 0 and self.player == 2:
                    send_mess(self, "Close\n")
                self.endGameTimer += self.endGameClock.tick(60) / 1000
                text = self.font_comic.render(self.endGameText,True,(255,255,255))
                self.screen.blit(text,text.get_rect(center=(self.screen.get_width()//2,self.screen.get_height()//2)))
                if self.endGameTimer >= 5:
                    running = False
            pygame.display.update()


def handle_hover(self, screen):
    mouse_pos = pygame.mouse.get_pos()
    card_display_place = (screen.get_width() // 2.5, screen.get_height() // 2.5)
    i = 0;
    for card in self.my_cards:
        card_rect = pygame.Rect((screen.get_width() * 0.26+(i*CARD_SIZE_X*0.9), screen.get_height() - CARD_SIZE_Y), (CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i+=1
    hero_rect = pygame.Rect(screen.get_width() * 0.025, screen.get_height() * 0.80,
                                                    CARD_SIZE_X, CARD_SIZE_Y)
    if hero_rect.collidepoint(mouse_pos):
     screen.blit(self.heroCard.image, card_display_place)

    hero_rect = pygame.Rect(screen.get_width() * 0.025, screen.get_height() * 0.025,
                                                    CARD_SIZE_X, CARD_SIZE_Y)
    if hero_rect.collidepoint(mouse_pos) :
        screen.blit(self.opp_heroCard.image, card_display_place)

    #battleground
    space_for_line = self.screen.get_height() // 8

    i = 0;
    for card in self.MyFrontRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 4) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i+=1
    i = 0;
    for card in self.MyMiddleRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 5) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i += 1
    i = 0;
    for card in self.MyBackRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 6) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i += 1
        # ================
    i = 0;
    for card in self.OppFrontRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 3) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i += 1
    i = 0;
    for card in self.OppMiddleRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 2) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i += 1
    i = 0;
    for card in self.OppBackRow:
        card_rect = pygame.Rect((screen.get_width() * 0.36 + (i * CARD_SIZE_X * 0.9),
                                 (space_for_line * 1) + (space_for_line - CARD_SIZE_Y)),(CARD_SIZE_X, CARD_SIZE_Y))
        if card_rect.collidepoint(mouse_pos):
            screen.blit(card.image, card_display_place)
        i += 1
    i = 0;
def handle_click(self,screen):
    mouse_pos = pygame.mouse.get_pos()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    i = 0;
    for card in self.my_cards:
        card_rect = (pygame.Rect((screen.get_width() * 0.26+(i*CARD_SIZE_X*0.9), screen.get_height() - CARD_SIZE_Y),
                                 (CARD_SIZE_X, CARD_SIZE_Y)))
        if card_rect.collidepoint(mouse_pos):
            self.stopHover = True
            if len(self.rects_to_display) > 0:
                self.rects_to_display = []
            space_for_line = self.screen.get_height() // 8
            if card.type == "front":
                self.rects_to_display.append((screen_width * 0.25,space_for_line * 4,
                                                 screen_width*0.75,space_for_line))
            elif card.type == "middle":
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 5,
                                              screen_width * 0.75, space_for_line))
            elif card.type == "back":
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 6,
                                              screen_width * 0.75, space_for_line))
            elif card.type == "mixed":
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 4,
                                              screen_width * 0.75, space_for_line))
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 5,
                                              screen_width * 0.75, space_for_line))
            elif card.name == "In Extremo":
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 4,
                                              screen_width * 0.75, space_for_line))
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 5,
                                              screen_width * 0.75, space_for_line))
                self.rects_to_display.append((screen_width * 0.25, space_for_line * 6,
                                              screen_width * 0.75, space_for_line))
            elif card.type == "weather":
                if card.name == "Mróz":
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 4,
                                                  screen_width * 0.75, space_for_line))
                elif card.name == "Deszcz":
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 6,
                                                  screen_width * 0.75, space_for_line))
                elif card.name == "Mgła":
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 5,
                                                  screen_width * 0.75, space_for_line))
                elif card.name == "Niebo":
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 4,
                                                  screen_width * 0.75, space_for_line))
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 5,
                                                  screen_width * 0.75, space_for_line))
                    self.rects_to_display.append((screen_width * 0.25, space_for_line * 6,
                                                  screen_width * 0.75, space_for_line))
            self.card_to_display = card.id
        i+=1
    hero_rect = pygame.Rect(screen.get_width() * 0.025, screen.get_height() * 0.80,
                                                    CARD_SIZE_X, CARD_SIZE_Y)
    if hero_rect.collidepoint(mouse_pos):
        if self.isHeroActive.strip() == 'T':
            self.hero_card_to_display = self.heroCard.id
            self.card_to_display = None
            self.stopHover = True

def falling_text(self,screen):
    if not (self.passed or self.endGame):
        if self.turn:
            text_surface = self.font_comic.render("Twoj ruch", True, "Green")
        else:
            text_surface = self.font_comic.render("Ruch przeciwnika", True, "Red")
        text_rect = text_surface.get_rect(center=(self.falling_text_x, screen.get_height()//2))
        if self.falling_text_x >= screen.get_width()//2 and (0 <= self.timer <= 3):
            self.timer += self.clock.tick(60) / 1000
        else:
            self.falling_text_x += 100
        self.screen.blit(text_surface, text_rect)

def checkIfMove(self):
    space_for_line = self.screen.get_height() // 8
    mouse_pos = pygame.mouse.get_pos()
    received_message = ''
    for rect in self.rects_to_display:
        rect_obj = pygame.Rect(rect)
        if rect_obj.collidepoint(mouse_pos):
            if rect[1] == (space_for_line * 4):
                received_message = send_mess(self, "M;" + str(self.card_to_display) + ";" + "f" + ";\n")
            elif rect[1] == (space_for_line*5):
                received_message = send_mess(self, "M;" + str(self.card_to_display) + ";" + "m" + ";\n")
            elif rect[1] == (space_for_line*6):
                received_message = send_mess(self, "M;" + str(self.card_to_display) + ";" + "b" + ";\n")
            if received_message.strip() == "Waiting":
                self.choosing = True
                received_message = send_mess(self, "GetStack\n").strip()
                #usunięcie karty
                send_mess(self, "R;"+ str(self.card_to_display) +";\n")
                self.cards_in_choose = []
                self.pos_in_choose = 0
                for id in received_message.split(";"):
                    if id != '':
                        self.cards_in_choose.append(self.all_Cards[int(id)])
            else:
                self.moved = True
    if self.hero_card_to_display is not None and self.isHeroActive.strip() == "T":
        received_message = send_mess(self, "H;" + str(self.hero_card_to_display) + ";"+"h"+";\n")
        if received_message.strip() == "WaitingForWeather":
            for i in self.all_Cards:
                if i.name == "Deszcz" or i.name == "Mgła" or i.name == "Mróz":
                    self.cards_in_choose.append(i)
            self.choosing = True
        else:
            self.moved = True

def prepare_battlefield(self):
    self.my_cards = []
    s = send_mess(self,"GetMyCards\n")
    add_cards_to_List(self,s,self.my_cards)

    s = send_mess(self, "GetOppCardsLength\n")
    self.opponent_cards_len = int(s)

    self.MyFrontRow = []
    s = send_mess(self,"GetMyFrontRow\n")
    add_cards_to_List(self, s, self.MyFrontRow)

    self.MyMiddleRow = []
    s = send_mess(self,"GetMyMiddleRow\n")
    add_cards_to_List(self, s, self.MyMiddleRow)

    self.MyBackRow = []
    s = send_mess(self,"GetMyBackRow\n")
    add_cards_to_List(self, s, self.MyBackRow)

    self.OppFrontRow = []
    s = send_mess(self,"GetOppFrontRow\n")
    add_cards_to_List(self, s, self.OppFrontRow)

    self.OppMiddleRow = []
    s = send_mess(self,"GetOppMiddleRow\n")
    add_cards_to_List(self, s, self.OppMiddleRow)

    self.OppBackRow = []
    s = send_mess(self,"GetOppBackRow\n")
    add_cards_to_List(self, s, self.OppBackRow)

    self.opp_heroCard = self.allHeroes[int(send_mess(self, "GetOppHeroCard\n"))]
    self.heroCard = self.allHeroes[int(send_mess(self, "GetMyHeroCard\n"))]

    self.hp = int(send_mess(self, "GetMyHP\n"))
    self.opp_hp = int(send_mess(self, "GetOppHP\n"))

    if self.hp == self.opp_hp == 0:
        self.endGame = True
        self.endGameText = "REMIS"
    elif self.hp == 0:
        self.endGame = True
        self.endGameText = "PORAŻKA"
    elif self.opp_hp == 0:
        self.endGame = True
        self.endGameText = "WYGRANA!!!"


    self.my_score = int(send_mess(self, "GetMyScore\n"))
    self.opp_score = int(send_mess(self, "GetOppScore\n"))

    self.myScores = send_mess(self,"GetMyScores\n")
    self.oppScores = send_mess(self,"GetOppScores\n")

    self.weather = send_mess(self, "GetWeather\n")

    self.toAttack = send_mess(self, "GetMultiplies\n").split(";")
    self.oppToAttack = send_mess(self, "GetOppMultiplies\n").split(";")

    self.isHeroActive = send_mess(self, "GetIsHeroActive\n")
    self.isOppHeroActive = send_mess(self, "GetIsOppHeroActive\n")

    mess = send_mess(self,"GetPassed\n")
    if mess[0] == 'T':
        self.passed = True
    else:
        self.passed = False
    mess = send_mess(self,"GetOppPassed\n")
    if mess[0] == 'T':
        self.oppPassed = True
    else:
        self.oppPassed = False

    turn = send_mess(self, "GetMyTurn\n")
    if int(turn.strip()) == 0:
        self.turn = False
    else:
        self.turn = True

    self.moved = False
    self.stopHover = False
    self.falling_text_x = 0
    self.timer = 0
    self.clock = pygame.time.Clock()
    self.falling_text_x = 0


def add_cards_to_List(self,mess,card_list):
     for i in mess.split(";"):
        if i.strip() != "":
            index = int(i)
            card_list.append(self.all_Cards[index])
def send_mess(self,mess):
    try:
        print("==================================")
        print("Send mess: " + mess)
        self.client.send(mess.encode("utf-8"))

        response = self.client.recv(1024)
        received_message = response.decode("utf-8")
        print("Received mess: " + received_message)
        return received_message

    except Exception as e:
        return ""

if __name__ == "__main__":

    connectionManager = ConnectionManager.ConnectionManager('192.168.1.26',8091)
    threading.Thread(target=connectionManager.start_server).start()
    pygame.init()
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main_instance = Game(window,'192.168.1.26' ,1)
    main_instance.run()


