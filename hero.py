import pygame
from bullet import Bullet
from bomb import Bomb 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

HERO_SPEED = 5

HERO_MAX_HP = 3

# Reload times (in seconds)
HERO_RELOAD_TIME = 0.3

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 128, 255))  # Blue color for hero
        self.rect = self.image.get_rect(center=(x, y))

        # Hero stats
        self.hp = HERO_MAX_HP
        self.speed = HERO_SPEED

        # Last direction the hero moved (default to up)
        self.last_dir_x = 0
        self.last_dir_y = -1

        # Shooting control
        self.can_shoot = True          # Can the hero shoot right now?
        self.bullet_in_flight = False  # Does the hero currently have a bullet on screen?
        self.next_shot_time = 0        # Next time (ms) hero can shoot again

        # Landing bomb control 
        self.can_land_bomb = True
        self.next_bomb_time = 0 

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
            self.next_shot_time = current_time + int(HERO_RELOAD_TIME * 1000)
            self.can_shoot = False

    def try_land_bomb(self, current_time, bomb_group):
        if self.can_land_bomb and current_time >= self.next_bomb_time:
            bomb = Bomb(
                x=self.rect.centerx,
                y=self.rect.centery,
                owner="hero",
                parent=self
            )
            bomb_group.add(bomb)

            self.next_bomb_time = current_time + int(HERO_RELOAD_TIME * 1000)
            self.can_land_bomb = False

    def update_shooting_cooldown(self, current_time):
        if current_time >= self.next_shot_time:
            self.can_shoot = True

    def update_landing_bomb_cooldown(self, current_time):
        if current_time >= self.next_bomb_time:
            self.can_land_bomb = True   