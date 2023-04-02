import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, ty):
        super().__init__()
        self.image = pygame.image.load('images/' + ty + '.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift