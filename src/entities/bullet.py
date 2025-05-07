import pygame
import math
from src.entities.base_entity import BaseEntity
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_SPEED

class Bullet(BaseEntity):
    def __init__(self, x, y, direction_x, direction_y, owner, parent):
        super().__init__(x, y)
        
        # Create bullet appearance
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0))  # Yellow bullet
        self.rect = self.image.get_rect(center=(x, y))

        # Normalize direction
        magnitude = math.hypot(direction_x, direction_y)
        if magnitude == 0:
            magnitude = 1
        self.direction_x = direction_x / magnitude
        self.direction_y = direction_y / magnitude

        # Override speed from BaseEntity
        self.speed = BULLET_SPEED
        self.owner = owner 
        self.parent = parent

    def update(self):
        self.rect.x += int(self.direction_x * self.speed)
        self.rect.y += int(self.direction_y * self.speed)
        
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.destroy()

    def destroy(self):
        super().destroy() 
        if self.parent:
            self.parent.bullet_in_flight = False