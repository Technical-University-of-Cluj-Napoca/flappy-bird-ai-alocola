import pygame
import config

class Ground:
    def __init__(self, win_width):
        self.image = config.BASE_IMG
        self.width = self.image.get_width()
        self.y = config.WIN_HEIGHT - 70 
        self.x1 = 0
        self.x2 = self.width
        self.vel = 4 

        self.rect = pygame.Rect(0, self.y, win_width, 100)

    def update(self,speed):
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))