import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/park.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.power = pygame.math.Vector2(0, 0)
        self.maxSpeed: int = 8
        self.isJumping: bool = False
        self.canMove: bool = True
        self.inertia: float = 0.2
        self.instantSpeed: int = 1
        self.gravity: float = 0.8
        self.jumpPower: int = 16
        self.isDebugVisible: bool = False
        self.DebugPressed = -1000


    def input(self):
        keys = pygame.key.get_pressed()
        lr = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.canMove:
                if self.power.x < self.maxSpeed:
                    self.power.x += self.instantSpeed
                    lr = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.canMove:
                if self.power.x > -self.maxSpeed:
                    self.power.x -= 1
                    lr = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not self.isJumping:
                self.power.y = -self.jumpPower
                self.isJumping = True

        if keys[pygame.K_F3]:
            tick = pygame.time.get_ticks()
            if tick - self.DebugPressed > 500:
                self.isDebugVisible = not self.isDebugVisible
                self.DebugPressed = tick

        if not lr:
            if abs(self.power.x) < 1:
                self.power.x = 0
                self.canMove = True
            elif self.power.x < 0:
                self.power.x += self.inertia
            elif self.power.x > 0:
                self.power.x -= self.inertia

    def update(self):
        self.input()

    def apply_gravity(self):
        self.power.y += self.gravity
        self.rect.y += self.power.y
