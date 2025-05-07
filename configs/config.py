import pygame
import os  # Added for path handling

pygame.init() 

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

pygame.display.set_caption("Game tông cửa 3 que")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

BACKGROUND = pygame.image.load("assets/images/war_background.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Frames per second
FPS = 60

HERO_SPEED = 5
HERO_MAX_HP = 5
HERO_RELOAD_TIME = 500
ENEMY_SPEED = 2.7
ENEMY_SHOOT_RANGE = 200
ENEMY_RELOAD_TIME = 2000
BULLET_SPEED = 7
EXPLOSION_DURATION = 300