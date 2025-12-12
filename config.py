import pygame
import os

pygame.init()
pygame.mixer.init()
WIN_WIDTH = 288
WIN_HEIGHT = 512
FPS = 30

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

BG_IMG = pygame.image.load(os.path.join("assets", "sprites", "background-day.png"))
BASE_IMG = pygame.image.load(os.path.join("assets", "sprites", "base.png"))
PIPE_IMG = pygame.image.load(os.path.join("assets", "sprites", "pipe_cola.png"))
raw_logo = pygame.image.load(os.path.join("assets", "sprites", "logo.png")).convert_alpha()
logo_width = 200  
scale_factor = logo_width / raw_logo.get_width()
logo_height = int(raw_logo.get_height() * scale_factor)
LOGO_IMG = pygame.transform.smoothscale(raw_logo, (logo_width, logo_height))
MEDAL_BRONZE = pygame.image.load(os.path.join("assets", "sprites", "medal-bronze.png")).convert_alpha()
MEDAL_SILVER = pygame.image.load(os.path.join("assets", "sprites", "medal-silver.png")).convert_alpha()
MEDAL_GOLD = pygame.image.load(os.path.join("assets", "sprites", "medal-gold.png")).convert_alpha()
MEDAL_PLATINUM = pygame.image.load(os.path.join("assets", "sprites", "medal-platinum.png")).convert_alpha()
SCORE_PANEL = pygame.image.load(os.path.join("assets", "sprites", "score_panel.png")).convert_alpha()




BIRD_IMGS = [
    pygame.image.load(os.path.join("assets", "sprites", "bluebird-upflap.png")),
    pygame.image.load(os.path.join("assets", "sprites", "bluebird-midflap.png")),
    pygame.image.load(os.path.join("assets", "sprites", "bluebird-downflap.png"))
]

pipes = []

AUDIO_PATH = os.path.join("assets", "audio")

SOUND_FLAP = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "wing.wav"))
SOUND_SCORE = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "point.wav"))
SOUND_HIT = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "hit.wav"))
SOUND_DIE = pygame.mixer.Sound(os.path.join(AUDIO_PATH, "alo_cola.wav"))

