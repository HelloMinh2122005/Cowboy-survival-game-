import pygame
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

BULLET_SPEED = 7

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, owner, parent):
        """
        :param parent: the entity (Hero or Enemy) that fired this bullet
                       so we can set bullet_in_flight = False when destroyed.
        """
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0))  # Yellow bullet
        self.rect = self.image.get_rect(center=(x, y))

        # Normalize direction
        magnitude = math.hypot(direction_x, direction_y)
        if magnitude == 0:
            magnitude = 1
        self.direction_x = direction_x / magnitude
        self.direction_y = direction_y / magnitude

        self.speed = BULLET_SPEED
        self.owner = owner  # "hero" or "enemy"
        self.parent = parent

    def update(self):
        # Move the bullet
        self.rect.x += int(self.direction_x * self.speed)
        self.rect.y += int(self.direction_y * self.speed)
        
        # Remove off-screen
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.destroy()

    def destroy(self):
        """Destroy bullet & notify parent that bullet is no longer in flight."""
        self.kill()
        if self.parent:
            self.parent.bullet_in_flight = False