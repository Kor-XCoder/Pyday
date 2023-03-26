import pygame
from settings import *

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, kx, ky):
        self.knockback = pygame.math.Vector2(kx, ky)
        super().__init__()
        self.image = pygame.image.load('images/spike.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift