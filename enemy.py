import pygame 
import math
from bullet import Bullet

from config import ENEMY_SPEED, ENEMY_SHOOT_RANGE,ENEMY_RELOAD_TIME


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('assets/tank.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (60, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        self.hp = 1
        self.speed = ENEMY_SPEED
        self.shoot_range = ENEMY_SHOOT_RANGE

        # Shooting control
        self.can_shoot = True
        self.bullet_in_flight = False
        self.next_shot_time = 0

    def update(self, hero, bullet_group, current_time):
        """Move toward hero unless within shooting range; if so, try to shoot."""
        if self.hp <= 0:
            return
        
        # Calculate distance to hero
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        # Calculate angle for both movement and rotation
        angle = math.atan2(dy, dx)
        
        rotation_angle = math.degrees(angle) + 90
        self.image = pygame.transform.rotate(self.original_image, -rotation_angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        if distance <= self.shoot_range:
            # Try shooting
            self.try_shoot(hero, bullet_group, current_time)
        else:
            # Move closer
            self.rect.x += int(self.speed * math.cos(angle))
            self.rect.y += int(self.speed * math.sin(angle))

    def try_shoot(self, hero, bullet_group, current_time):
        """
        Attempt to shoot at hero if:
         - can_shoot is True
         - no bullet in flight
         - current_time >= next_shot_time
        """
        if self.can_shoot and not self.bullet_in_flight and current_time >= self.next_shot_time:
            # Direction from enemy to hero
            dx = hero.rect.centerx - self.rect.centerx
            dy = hero.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance == 0:
                distance = 1  # Avoid division by zero
            direction_x = dx / distance
            direction_y = dy / distance

            # Create bullet
            bullet = Bullet(
                x=self.rect.centerx,
                y=self.rect.centery,
                direction_x=direction_x,
                direction_y=direction_y,
                owner="enemy",
                parent=self
            )
            bullet_group.add(bullet)

            self.bullet_in_flight = True
            self.next_shot_time = current_time + int(ENEMY_RELOAD_TIME)
            self.can_shoot = False

    def update_shooting_cooldown(self, current_time):
        """If current_time >= next_shot_time, can shoot again (and bullet_in_flight is False)."""
        if current_time >= self.next_shot_time:
            self.can_shoot = True