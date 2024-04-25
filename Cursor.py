import pygame
class Cursor:
    def __init__(self):
        self.spr = pygame.transform.scale(pygame.image.load("data/cursor/test2.png"),(128,128))
        self.x = 0
        self.y = 0
    def draw(self,window):
        window.blit(self.spr,(self.x,self.y))
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.x -= 48
        self.y -= 48
