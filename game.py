import pygame
import menu
import os

# Inicjalizacja Pygame
pygame.init()

# Ustawienia menu
font_path = os.path.join("data", "fonts", "Gothic_Ingame_Offiziell.ttf")  # Ścieżka do pliku czcionki
menu_items = ["Rozpocznij grę", "Exit"]
main_menu = menu.Menu(font_path, menu_items)

# Pobranie rozmiaru ekranu
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gothic Gwint")

#Game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #LMB
                mouse_pos = pygame.mouse.get_pos()
                if main_menu.handle_click(mouse_pos):  # S
                    running = False

    # Wyczyszczenie ekranu
    window.fill((255, 255, 255))
    # Rysowanie menu
    main_menu.draw(window)

    # Zaktualizowanie ekranu
    pygame.display.flip()

# Zamknięcie Pygame
pygame.quit()
