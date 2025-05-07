import pygame
from bullet import Bullet
from configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, HERO_SPEED, HERO_MAX_HP, HERO_RELOAD_TIME

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the image
        self.original_image = pygame.image.load('assets/vietnam_tank.png').convert_alpha()
        # Scale the image if needed
        self.original_image = pygame.transform.scale(self.original_image, (90, 120))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
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
            
            # Rotate the image to face the direction of movement
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
                
            self.image = pygame.transform.rotate(self.original_image, angle)
            # Update rect position to maintain center position
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

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
        """
        Attempt to shoot if:
         - The hero can shoot right now (self.can_shoot)
         - No bullet in flight
        """
        if self.can_shoot and current_time >= self.next_shot_time:
            # Create a bullet in the last move direction
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

            # Set next time to shoot (cooldown)
            self.next_shot_time = current_time + int(HERO_RELOAD_TIME)
            self.can_shoot = False

    def update_shooting_cooldown(self, current_time):
        if current_time >= self.next_shot_time:
            self.can_shoot = True
