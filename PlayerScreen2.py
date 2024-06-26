import pygame
import os
import socket
import game
from Cursor import Cursor
from ConnectionManager import ConnectionManager
from threading import Thread


class PlayerScreen2:
    def __init__(self, screen):
        self.background_image = pygame.transform.scale(pygame.image.load(
            "data/connect.jpg"), (screen.get_width(), screen.get_height()))
        self.background_rect = self.background_image.get_rect()
        self.font_gothic = pygame.font.Font(os.path.join(
            "data", "fonts", "Gothic_Ingame_Offiziell.ttf"), 60)
        self.cursor = Cursor()
        self.cursor.changeType(2)
        self.display_text = "Oczekiwanie na polaczenie..."
        self.back_text = self.font_gothic.render("Wroc", True, "white")
        self.back_text_rect = self.back_text.get_rect(
            topleft=(20, 20))

        try:
            self.connectionManager = ConnectionManager(self.getLocalIP(), 8091)
            self.server_thread = Thread(
                target=self.connectionManager.start_server)
            self.server_thread.start()
        except Exception as e:
            print(e)

        running = True
        while running:
            screen.fill((255, 255, 255))
            screen.blit(self.background_image, self.background_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.back_text_rect.collidepoint(
                            pygame.mouse.get_pos()):
                        running = False

            text_surface = self.font_gothic.render(
                "Oczekiwanie na polaczenie...", True, "white")
            text_rect = text_surface.get_rect(
                center=(
                    screen.get_width() // 2,
                    screen.get_height() // 2))
            screen.blit(text_surface, text_rect)

            screen.blit(self.back_text, self.back_text_rect)

            self.cursor.update()
            self.cursor.draw(screen)

            self.handle_hover()

            if (self.connectionManager.start == 2):
                ip = self.getLocalIP()
                g = game.Game(screen, ip, 2)
                g.run()
                self.connectionManager.stop_server()
                self.server_thread.join()
                running = False
            elif self.connectionManager.start == 3:
                running = False

            pygame.display.update()

    def handle_hover(self):

        was_cursor_on_text = False
        if self.back_text_rect.collidepoint(pygame.mouse.get_pos()):
            self.back_text = self.font_gothic.render("Wroc", True, "green")
            was_cursor_on_text = True
        else:
            self.back_text = self.font_gothic.render("Wroc", True, "white")

        if was_cursor_on_text:
            self.cursor.changeType(1)
        else:
            self.cursor.changeType(2)

    def getLocalIP(self):
        #return "26.83.23.199"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()
            return local_ip
        except Exception as e:
            print(e)
            return None
