import pygame 
import math
from src.entities.bullet import Bullet
from src.entities.base_entity import BaseEntity
from configs.config import ENEMY_SPEED, ENEMY_SHOOT_RANGE, ENEMY_RELOAD_TIME

class Enemy(BaseEntity):
    def __init__(self, x, y):
        # Call BaseEntity's init with image path and size
        super().__init__(
            x=x, 
            y=y, 
            image_path='assets/images/tank.png',
            size=(60, 80)
        )
        
        # Enemy-specific attributes
        self.hp = 1
        self.speed = ENEMY_SPEED
        self.shoot_range = ENEMY_SHOOT_RANGE

        # Initialize shooting capabilities
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
        
        # Use BaseEntity's rotate_image method instead
        rotation_angle = math.degrees(angle) + 90
        self.rotate_image(-rotation_angle)

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