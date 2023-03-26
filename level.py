import pygame
from tiles import Tile
from settings import *
from player import Player

class Level:
    def __init__(self, lv_data, surface):
        # Level Setup
        self.tiles = None
        self.player = None
        self.display_surface = surface
        self.setup(lv_data)
        self.world_shift = 0
        self.Maracle = None
        self.map = None

    def setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((x * tile_size, y * tile_size), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.Maracle = Player((x * tile_size, y * tile_size))
                    self.player.add(self.Maracle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.power.x

        limit = screen_width / 4

        if player_x < limit and direction_x < 0:
            self.world_shift = round(player.power.x)
            # player.maxSpeed = 0
        elif player_x > screen_width - limit and direction_x > 0:
            self.world_shift = round(player.power.x)
            # player.maxSpeed = 0
        else:
            self.world_shift = 0
            # player.maxSpeed = 8

    def run(self):
        self.scroll_x()

        self.tiles.update(-self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.check_horizontal()
        self.check_vertical()
        self.player.draw(self.display_surface)

    def check_horizontal(self):
        player = self.player.sprite

        if self.world_shift == 0:
            player.rect.x += player.power.x

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.power.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.power.x > 0:
                    player.rect.right = sprite.rect.left
        player.rect.x = max(player.rect.x, 0) # prevent player from going offscreen to the left
        player.rect.x = min(player.rect.x, screen_width - player.rect.width) # prevent player from going offscreen to the right

    def check_vertical(self):
        player = self.player.sprite
        player.apply_gravity() # updating y position and apply gravity

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.power.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.power.y = 0
                    player.isJumping = False
                elif player.power.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.power.y = 0
        if player.isJumping or player.power.y > 0:
            player.power.y = min(player.power.y, 20)

    def checkDebug(self):
        return self.player.sprite.isDebugVisible
