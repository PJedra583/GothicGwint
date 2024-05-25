import pygame
import random

class GraphicEffects:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.background_color = (0, 0, 0)
        self.fog_particles = []
        self.fogArea = None

    def make_fog(self, area, fog_particle_count=100):
        x_min, y_min, x_max, y_max = area
        self.fogArea = area

        for i in range(fog_particle_count):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            size = random.randint(20, 50)
            opacity = random.randint(100, 100)  # Różna przezroczystość cząsteczek mgły
            self.fog_particles.append([x, y, size, opacity])

    def draw_fog(self):
        x_min, y_min, x_max, y_max = self.fogArea

        for particle in self.fog_particles:
            particle[1] += random.uniform(-0.5, 0.5)
            particle[0] += random.uniform(-0.5, 0.5)

            if particle[1] < y_min:
                particle[1] = y_min
            if particle[1] > y_max:
                particle[1] = y_max
            if particle[0] < x_min:
                particle[0] = x_min
            if particle[0] > x_max:
                particle[0] = x_max

            surface = pygame.Surface((particle[2], particle[2]), pygame.SRCALPHA)
            fog_color = (200, 200, 200, particle[3])
            # w połowie surface rysuje koło o promieniu połowy rozmiaru
            pygame.draw.circle(surface, fog_color, (particle[2] // 2, particle[2] // 2), particle[2] // 2)
            # rysowanie względem ekranu
            self.screen.blit(surface, (particle[0] - particle[2] // 2, particle[1] - particle[2] // 2))

  #
  # surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
  #                       pygame.draw.rect(surface, (255, 255, 0, 10), rect)
  #                       self.screen.blit(surface,(rect[0],rect[1]))
# Użycie klasy GraphicEffects
pygame.init()

# Ustawienia ekranu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Symulacja Mgły")

# Tworzenie instancji GraphicEffects
effects = GraphicEffects(screen)

# Określenie obszaru mgły
space_for_line = screen_height // 8
fog_area = (int(screen_width * 0.25), int(space_for_line * 4), int(screen_width * 0.75), int(space_for_line * 5))

# Inicjalizacja mgły
effects.make_fog(fog_area)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rysowanie tła
    screen.fill(effects.background_color)

    # Aktualizacja i rysowanie mgły
    effects.draw_fog()

    # Aktualizacja ekranu
    pygame.display.flip()

    # Opóźnienie dla lepszej wizualizacji
    pygame.time.delay(30)

pygame.quit()
