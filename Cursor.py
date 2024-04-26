import pygame
class Cursor:
    def __init__(self):
        self.spr1 = pygame.transform.scale(pygame.image.load("data/cursor/test1.png"),(128,128))
        self.spr2 = pygame.transform.scale(pygame.image.load("data/cursor/test2.png"),(128,128))
        self.spr = self.spr1;
        self.x = 0
        self.y = 0
    def draw(self,window):
        window.blit(self.spr,(self.x,self.y))
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.x -= 48
        self.y -= 48
    def changeType(self,version):
        if version == 1:
         self.spr = self.spr1
        else:
         self.spr = self.spr2
