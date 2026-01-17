import pygame
import random
import config
from logic import brain

class Player:
    def __init__(self):
        self.image_index = 0
        self.images = config.BIRD_IMGS
        self.image = self.images[self.image_index]
        
        self.rect = self.image.get_rect()
        self.rect.center = (50, int(config.WIN_HEIGHT / 2))

        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        rotation = self.vel * -2
        rotated_image = pygame.transform.rotate(self.image, rotation)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            self.vel += 0.3
            self.rect.y += int(self.vel)
            
            if self.vel > 8:
                self.vel = 8
            
            if self.flap:
                self.image_index = (self.image_index + 1) % 3
                self.image = self.images[self.image_index]

            if self.vel >= -2:
                self.flap = False

            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5 
            config.SOUND_FLAP.play()


    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def ground_collision(self, ground):
        if self.rect.bottom >= ground.y:
            return True
        return False

    def sky_collision(self):
        return bool(self.rect.y < 0)

    def pipe_collision(self):
        for p in config.pipes:
            if p.collide(self):
                return True
        return False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p
        return config.pipes[0] if config.pipes else None

    def look(self):
        if config.pipes:
            pipe = self.closest_pipe()
            if pipe:
                self.vision[0] = max(0, self.rect.center[1] - pipe.top_rect.bottom) / 500
                pygame.draw.line(config.WINDOW, (255, 0, 0), self.rect.center, 
                                 (self.rect.center[0], pipe.top_rect.bottom))

                self.vision[1] = max(0, pipe.x - self.rect.center[0]) / 500
                pygame.draw.line(config.WINDOW, (255, 0, 0), self.rect.center, 
                                 (pipe.x, self.rect.center[1]))

                self.vision[2] = max(0, pipe.bottom_rect.top - self.rect.center[1]) / 500
                pygame.draw.line(config.WINDOW, (255, 0, 0), self.rect.center, 
                                 (self.rect.center[0], pipe.bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone