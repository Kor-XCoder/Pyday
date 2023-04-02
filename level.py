import pygame
from tiles import Tile
from spikes import Spike
from settings import *
from player import Player
from exit import Exit

class Level:
    def __init__(self, lv_data, surface):
        # Level Setup
        self.ex = None
        self.exits = None
        self.spikes = None
        self.tiles = None
        self.player = None
        self.display_surface = surface
        self.setup(lv_data)
        self.world_shift = 0
        self.Maracle = None
        self.map = None
        self.ending = False

    def setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.exits = pygame.sprite.GroupSingle()
        plus = screen_real_height - screen_height

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((x * tile_size, plus + y * tile_size), tile_size, 'stone')
                    self.tiles.add(tile)
                elif cell == '1':
                    tile = Tile((x * tile_size, plus + y * tile_size), tile_size, 'grass')
                    self.tiles.add(tile)
                elif cell == '2':
                    tile = Tile((x * tile_size, plus + y * tile_size), tile_size, 'dirt')
                    self.tiles.add(tile)
                elif cell == 'A':
                    spike = Spike((x * tile_size, plus + y * tile_size), 17, 13, 'lava')
                    self.spikes.add(spike)
                elif cell == 'P':
                    self.Maracle = Player((x * tile_size, plus + y * tile_size))
                    self.player.add(self.Maracle)
                elif cell == 'B':
                    spike = Spike((x * tile_size, plus + y * tile_size), 17, 13, 'lava_block')
                    self.spikes.add(spike)
                elif cell == 'C':
                    spike = Spike((x * tile_size, plus + y * tile_size), 17, 30, 'lava')
                    self.spikes.add(spike)
                elif cell == 'E':
                    self.ex = Exit((x * tile_size, plus + y * tile_size))
                    self.exits.add(self.ex)


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

        self.spikes.update(-self.world_shift)
        self.spikes.draw(self.display_surface)

        self.player.update()

        self.check_horizontal()
        self.check_vertical()

        self.exits.update(-self.world_shift)
        self.exits.draw(self.display_surface)
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

        for spike in self.spikes.sprites():
            if spike.rect.colliderect(player.rect):
                player.power.x = -spike.knockback.x
                player.power.y = -spike.knockback.y
                player.isJumping = True
                player.canMove = False
                player.isSpiking = True


        if self.exits.sprite.rect.colliderect(player.rect):
            self.ending = True

        player.rect.x = max(player.rect.x, 0)
        player.rect.x = min(player.rect.x, screen_width - player.rect.width)

    def check_vertical(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.power.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.power.y = 0
                    if player.isSpiking:
                        if abs(player.power.x) <= 1.5:
                            player.isJumping = False
                            player.canMove = True
                            player.isSpiking = False
                    else:
                        player.isJumping = False
                        player.canMove = True
                elif player.power.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.power.y = 0

        for spike in self.spikes.sprites():
            if spike.rect.colliderect(player.rect):
                player.power.x = -spike.knockback.x
                player.power.y = -spike.knockback.y
                player.isJumping = True
                player.canMove = False
                player.isSpiking = True
        if player.isJumping or player.power.y > 0:
            player.power.y = min(player.power.y, 20)

        if self.exits.sprite.rect.colliderect(player.rect):
            self.ending = True

    def checkDebug(self):
        return self.player.sprite.isDebugVisible
