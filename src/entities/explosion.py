import pygame
from src.entities.base_entity import BaseEntity
from src.configs.config import EXPLOSION_DURATION

class Explosion(BaseEntity):
    def __init__(self, x, y):
        super().__init__(
            x=x, 
            y=y, 
            image_path='assets/images/explosion.png',
            size=(100, 100)
        )
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self, current_time):
        if current_time - self.spawn_time > EXPLOSION_DURATION:
            self.destroy() 