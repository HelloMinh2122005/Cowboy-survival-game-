import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, parent):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))  # Black bomb
        self.rect = self.image.get_rect(center=(x, y))

        self.owner = owner  # "hero" or "enemy"
        self.parent = parent

        # Set a timer to explode after 1 second (1000 milliseconds)
        self.explode_time = pygame.time.get_ticks() + 1000

    def update(self, current_time, all_sprites):
        if current_time >= self.explode_time:
            self.explode(all_sprites)

    def explode(self, all_sprites):
        explosion_area = pygame.Rect(self.rect.x - 20, self.rect.y - 20, 100, 100)
        for sprite in all_sprites:
            if sprite != self and explosion_area.colliderect(sprite.rect):
                sprite.kill()
        
        # Create a yellow explosion effect
        explosion = pygame.Surface((50, 50))
        explosion.fill((255, 255, 0))  # Yellow explosion
        explosion_rect = explosion.get_rect(center=self.rect.center)
        
        # Blit the explosion to the screen
        screen = pygame.display.get_surface()
        screen.blit(explosion, explosion_rect)
        pygame.display.flip()
        
        # Wait for 3 milliseconds
        pygame.time.delay(2)
        
        self.kill()