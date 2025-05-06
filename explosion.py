import pygame
from config import EXPLOSION_DURATION

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/explosion.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self, current_time):
        # Remove explosion after duration expires
        if current_time - self.spawn_time > EXPLOSION_DURATION:
            self.kill()