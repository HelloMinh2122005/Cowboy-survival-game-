import pygame
from src.entities.bullet import Bullet
from src.entities.base_entity import BaseEntity
from configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, HERO_SPEED, HERO_MAX_HP, HERO_RELOAD_TIME

class Hero(BaseEntity):
    def __init__(self, x, y):
        # Call BaseEntity's init with image path and size
        super().__init__(
            x=x, 
            y=y, 
            image_path='assets/images/vietnam_tank.png',
            size=(90, 120)
        )
        
        # Hero stats
        self.hp = HERO_MAX_HP
        self.speed = HERO_SPEED
        
        # Last direction the hero moved (default to up)
        self.last_dir_x = 0
        self.last_dir_y = -1
        
        # Shooting control
        self.can_shoot = True
        self.bullet_in_flight = False
        self.next_shot_time = 0
        
    def handle_movement(self, keys_pressed):
        """Update hero position & store the last non-zero movement direction."""
        dx, dy = 0, 0
        if keys_pressed[pygame.K_UP]:
            dy = -1
        elif keys_pressed[pygame.K_DOWN]:
            dy = 1
        if keys_pressed[pygame.K_LEFT]:
            dx = -1
        elif keys_pressed[pygame.K_RIGHT]:
            dx = 1

        # If the hero moves, update last_dir_x and last_dir_y
        if dx != 0 or dy != 0:
            self.last_dir_x = dx
            self.last_dir_y = dy
            
            # Calculate angle based on movement direction
            angle = 0
            if dx == 0 and dy == -1:  # Up
                angle = 0
            elif dx == 0 and dy == 1:  # Down
                angle = 180
            elif dx == -1 and dy == 0:  # Left
                angle = 90
            elif dx == 1 and dy == 0:  # Right
                angle = 270
            elif dx == -1 and dy == -1:  # Up-left
                angle = 45
            elif dx == 1 and dy == -1:  # Up-right
                angle = 315
            elif dx == -1 and dy == 1:  # Down-left
                angle = 135
            elif dx == 1 and dy == 1:  # Down-right
                angle = 225
                
            # Use BaseEntity's rotate_image method
            self.rotate_image(angle)

        # Move the hero
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Keep hero within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def try_shoot(self, current_time, bullet_group):
        if self.can_shoot and current_time >= self.next_shot_time:
            bullet = Bullet (
                x=self.rect.centerx,
                y=self.rect.centery,
                direction_x=self.last_dir_x,
                direction_y=self.last_dir_y,
                owner="hero",
                parent=self
            )
            bullet_group.add(bullet)
            self.bullet_in_flight = True

            self.next_shot_time = current_time + int(HERO_RELOAD_TIME)
            self.can_shoot = False