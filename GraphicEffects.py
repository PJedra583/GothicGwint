import pygame
import random


class GraphicEffects:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.rain_color = (0, 0, 255)
        self.snow_color = (255, 255, 255)
        self.snow_flakes = []
        self.rain_drops = []
        self.fog_particles = []


    def make_rain(self, area, rain_drop_count=100):
        x_min, y_min, x_max, y_max = area
        self.rainArea = area

        for i in range(rain_drop_count):
            x = random.randint(x_min, x_max)
            y = random.randint(0, y_max)
            speed = random.randint(4, 16)
            self.rain_drops.append([x, y, speed])

    def draw_rain(self):
        x_min, y_min, x_max, y_max = self.rainArea

        for drop in self.rain_drops:
            drop[1] += drop[2]
            #kropla spada gdzie indziej
            if drop[1] > self.screen_height:
                drop[1] = 0
                drop[0] = random.randint(x_min, x_max)
                drop[2] = random.randint(4, 16)
        for drop in self.rain_drops:
            if y_min <= drop[1] <= y_max:
                pygame.draw.line(self.screen, self.rain_color, (drop[0], drop[1]), (drop[0], drop[1] + 10), 2)

    def make_snow(self, area, snow_flake_count=1000):
        x_min, y_min, x_max, y_max = area
        self.snowArea = area

        for i in range(snow_flake_count):
            x = random.randint(x_min, x_max)
            y = y_min - 20
            speed = random.uniform(1, 4)
            size = random.randint(2, 5)
            self.snow_flakes.append([x, y, speed, size])
    def draw_snow(self):
        x_min, y_min, x_max, y_max = self.snowArea

        for flake in self.snow_flakes:
            flake[1] += flake[2]
            if flake[1] > y_max:
                flake[1] = random.randint(y_min - 20, y_min)
                flake[0] = random.randint(x_min, x_max)
                flake[2] = random.uniform(1, 4)
                flake[3] = random.randint(2, 5)

        for flake in self.snow_flakes:
            if y_min+flake[3] <= flake[1] <= y_max-flake[3]:
                pygame.draw.circle(self.screen, self.snow_color, (flake[0], flake[1]), flake[3])
    def make_fog(self, area, fog_particle_count=100):
        x_min, y_min, x_max, y_max = area
        self.fogArea = area

        for i in range(fog_particle_count):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            size = random.randint(20, 50)
            opacity = random.randint(30, 70)
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