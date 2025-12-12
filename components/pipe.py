import pygame
import random
import config

class Pipes:
    GAP = 50  
    VEL = 4    

    def __init__(self, x,speed):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        
        self.PIPE_TOP = pygame.transform.flip(config.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = config.PIPE_IMG
        
        self.passed = False
        self.set_height(speed)

    def set_height(self,speed):
        self.height = random.randrange(100, 290)
        self.top = self.height - self.PIPE_TOP.get_height()
        gap = self.GAP + max(0, speed - 4) * 2.5   # widen by 2.5px per speed step
        self.bottom = self.height + gap
        
        self.top_rect = pygame.Rect(self.x, self.top,
                            self.PIPE_TOP.get_width(),
                            self.PIPE_TOP.get_height())

        self.bottom_rect = pygame.Rect(self.x, self.bottom,
                                    self.PIPE_BOTTOM.get_width(),
                                    self.PIPE_BOTTOM.get_height())


    def update(self,speed):
        self.x -= speed
        
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        

    def draw(self, window):
        self.top_rect.topleft = (self.x, self.top)
        self.bottom_rect.topleft = (self.x, self.bottom)
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.rect.x, self.top - bird.rect.y)
        bottom_offset = (self.x - bird.rect.x, self.bottom - bird.rect.y)

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False