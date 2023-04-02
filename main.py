import sys
import pygame
import math
from settings import *
from level import Level
import random

# Pygame Settings
pygame.init()
pygame.display.set_caption("AlldayMo")

def getMiddle(width):
    return (screen_width - width) // 2

def getMiddleHeight(height):
    return (screen_real_height - height) // 2

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
fade_surface = pygame.Surface((screen_width, screen_real_height))
fade_surface.fill((0, 0, 0))
fade_alpha = 0
fade_surface.set_alpha(fade_alpha)

# screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
delay = 700
level = Level(level1, screen)
isGameOver: bool = False
scene: str = 'main'
font = pygame.font.SysFont("arial", 30, True, False)
SpeedText = font.render('Speed: 0', True, (255, 255, 255))


StartButton_image = pygame.image.load('images/start-button.png')
StartButton_image = pygame.transform.scale(StartButton_image, (320, 100))
background_image = pygame.image.load('images/logo_back3.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_real_height))
PixelFont = pygame.font.Font('font/SPACEBOY.TTF', 100)
PixelMediumFont = pygame.font.Font('font/SPACEBOY.TTF', 64)
PixelSmallFont = pygame.font.Font('font/SPACEBOY.TTF', 30)
logo = PixelFont.render('AlldayMo', True, (255, 222, 10))
made_by_coder = PixelSmallFont.render('Made By Coder#4287', True, (0, 0, 0))
game_back = pygame.image.load('images/game_back.jpeg')
game_back = pygame.transform.scale(game_back, (screen_width, screen_height))
StartButton_Rect = StartButton_image.get_rect(topleft=(getMiddle(StartButton_image.get_width()), 520))

ThankYou = PixelMediumFont.render('', True, (255, 255, 255))
ThankYou_Rect = ThankYou.get_rect(topleft=(getMiddle(ThankYou.get_width()), getMiddleHeight(ThankYou.get_height())))

Special = PixelSmallFont.render('', True, (255, 255, 255))
ThanksTo = PixelMediumFont.render('', True, (255, 255, 255))

def main():
    global isGameOver, scene, fade_alpha, fade_surface, ThankYou, delay, Special, ThanksTo
    level.setup(level1)
    while not isGameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameOver = True

        if scene == 'main':
            # screen.fill((0, 7, 102))
            screen.blit(background_image, (0, 0))
            screen.blit(logo, (getMiddle(logo.get_width()), 20))
            screen.blit(made_by_coder, (getMiddle(made_by_coder.get_width()), 150))
            screen.blit(StartButton_image, (getMiddle(StartButton_image.get_width()), 520))
            if StartButton_Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                # print(pygame.time.get_ticks())
                scene = 'game'
        elif scene == 'game':
            game()
        elif scene == 'ending':
            screen.blit(fade_surface, (0, 0))

            fade_alpha += 0.1
            fade_surface.set_alpha(fade_alpha)

            if fade_alpha >= 64:
                scene = 'real_ending'
        elif scene == 'real_ending':
            T_text = 'Thank you for playing!'
            C_text = 'Code by Coder#4287'
            Th_text = 'Special Thanks to Maracle. Antaewon. Allday!'
            cur = ''
            screen.fill('black')
            fade_surface.set_alpha(0)
            screen.blit(fade_surface, (0, 0))
            for ch in T_text:
                screen.fill('black')
                cur += ch
                ThankYou = PixelMediumFont.render(cur, True, (255, 255, 255))
                screen.blit(ThankYou, (getMiddle(ThankYou.get_width()), getMiddleHeight(ThankYou.get_height()) - 30))
                pygame.display.update()

                delay = random.randrange(100, 400)
                clock.tick(1000 // delay)
                pygame.time.wait(delay)

            ThankYou = PixelMediumFont.render(T_text, True, (255, 255, 255))

            cur = ''
            for ch in C_text:
                screen.fill('black')
                screen.blit(ThankYou, (getMiddle(ThankYou.get_width()), getMiddleHeight(ThankYou.get_height()) - 30))
                cur += ch
                Special = PixelSmallFont.render(cur, True, (255, 255, 255))
                screen.blit(Special, (getMiddle(Special.get_width()), getMiddleHeight(Special.get_height()) + 100))
                pygame.display.update()

                delay = random.randrange(100, 400)
                clock.tick(1000 // delay)
                pygame.time.wait(delay)

            Special = PixelSmallFont.render(C_text, True, (255, 255, 255))
            cur = ''

            for ch in Th_text:
                screen.fill('black')
                screen.blit(ThankYou, (getMiddle(ThankYou.get_width()), getMiddleHeight(ThankYou.get_height()) - 30))
                screen.blit(Special, (getMiddle(Special.get_width()), getMiddleHeight(Special.get_height()) + 100))
                cur += ch
                ThanksTo = PixelSmallFont.render(cur, True, (255, 255, 255))
                screen.blit(ThanksTo, (getMiddle(ThanksTo.get_width()), getMiddleHeight(ThanksTo.get_height()) + 150))
                pygame.display.update()

                delay = random.randrange(100, 400)
                clock.tick(1000 // delay)
                pygame.time.wait(delay)

            scene = 'done'

        pygame.display.update()


    # Quit Pygame
    pygame.quit()
    sys.exit()

def game():
    global screen, level, SpeedText, scene
    # Update game logic and draw graphics here
    screen.fill((125, 229, 255))
    # screen.blit(game_back, (0, 0))

    level.run()

    if level.ending:
        scene = 'ending'
        return

    player = level.player.sprite
    if level.checkDebug():
        SpeedText = font.render('Speed: ' + str(round(player.power.x, 1)), True, (255, 255, 255))
        screen.blit(SpeedText, (5, 10))

    pygame.display.update()
    clock.tick(60)


main()
