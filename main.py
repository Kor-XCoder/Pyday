import sys
import pygame
import math
from settings import *
from level import Level

# Pygame Settings
pygame.init()
def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    level = Level(level1, screen)
    isGameOver: bool = False
    font = pygame.font.SysFont("arial", 30, True, False)
    SpeedText = font.render('Speed: 0', True, (255, 255, 255))

    level.setup(level1)
    while not isGameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameOver = True

        # Update game logic and draw graphics here
        screen.fill('black')
        level.run()
        player = level.player.sprite
        if level.checkDebug():
            SpeedText = font.render('Speed: ' + str(round(player.power.x, 1)), True, (255, 255, 255))
            screen.blit(SpeedText, (5, 10))

        pygame.display.update()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()


main()
