import pygame
import os

class Menu:
    def __init__(self):
        font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Font z gothica
        self.font = pygame.font.Font(font_path, 30)
        self.color = (255, 255, 255)
        self.items = ["Rozpocznij gre","Samouczek","Tworcy gry","Exit"]

    def draw(self, screen):
        menu_surface = pygame.Surface((screen.get_width(), 30))
        menu_surface.fill((0, 0, 0))
        for i, item in enumerate(self.items):
            text = self.font.render(item, True, self.color)
            menu_surface.blit(text, (10 + i * 150, 5))
        screen.blit(menu_surface, (0, 0))

    def handle_click(self, mouse_pos):
        if mouse_pos[1] < 30:  # Sprawdzenie czy kliknięto w obszarze paska menu
            if 0 <= mouse_pos[0] < 150:  # Sprawdzenie czy kliknięto na pierwszą opcję
                if self.items[0] == "Rozpocznij grę":  # Sprawdzenie czy pierwsza opcja to "Rozpocznij grę"
                    self.items = ["Exit"]  # Zmiana opcji menu na "Exit"
                    return True
            elif 150 <= mouse_pos[0] < 300:  # Sprawdzenie czy kliknięto na drugą opcję
                if self.items[1] == "Exit":  # Sprawdzenie czy druga opcja to "Exit"
                    return False
