import pygame
import sys
from src.entities.hero import Hero
from src.entities.explosion import Explosion
from src.configs.config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BACKGROUND
import ui.hud as hud
from src.systems.level import LevelManager
from src.systems.collision import CollisionManager

class Game:
    def __init__(self):
        # Groups for sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Create hero
        self.hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.hero)
        
        # Initialize level manager
        self.level_manager = LevelManager()
        self.level_manager.setup_enemy_timer()
        
        # Initialize collision manager
        self.collision_manager = CollisionManager(
            self.hero, 
            self.all_sprites, 
            self.enemies, 
            self.bullets, 
            self.explosions, 
            self.level_manager
        )
        
        self.running = True

    def handle_events(self, current_time):
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.hero.try_shoot(current_time, self.bullets)
                    self.all_sprites.add(self.bullets)
                elif event.key == pygame.K_p:
                    choice = hud.show_game_pause_popup(
                        hud.screen
                    )
                    if choice == "exit":
                        self.running = False

            # Spawn enemy event
            if event.type == pygame.USEREVENT + 1:
                if self.level_manager.remaining_enemies > 0:
                    self.level_manager.spawn_enemy(self.enemies, self.all_sprites)

    def update(self, current_time):
        # Update hero
        keys_pressed = pygame.key.get_pressed()
        self.hero.handle_movement(keys_pressed)
        self.hero.update_shooting_cooldown(current_time)

        # Update enemies
        for enemy in self.enemies:
            enemy.update_shooting_cooldown(current_time)
            enemy.update(self.hero, self.bullets, current_time)

        self.all_sprites.add(self.bullets)
        
        # Update bullets
        self.bullets.update()

        # Check collisions and update game state
        game_status = self.collision_manager.update(hud.screen)
        
        if not game_status["running"]:
            self.running = False
        
        if game_status["reset"]:
            self.hero = self.collision_manager.reset_game()
            return False  # Signal to skip the rest of the update
            
        # Update explosions
        for explosion in self.explosions:
            explosion.update(current_time)
            
        return True  # Continue with the update

    def render(self):
        hud.screen.blit(BACKGROUND, (0, 0))

        # Draw all sprites
        self.all_sprites.draw(hud.screen)
        
        hud.display_hud(
            hud.screen, 
            self.hero.hp, 
            self.level_manager.current_level + 1
        )
        
        pygame.display.flip()

    def show_menu_screen(self):
        choice = hud.show_game_image_main_menu(hud.screen) and hud.show_vid_next_level(hud.screen, 0) and hud.show_game_next_level(hud.screen, 0)
        if choice == "play":
            self.running = True
        elif choice == "exit":
            self.running = False

    def run(self):
        # Show the main menu screen
        self.show_menu_screen()
        
        while self.running:
            dt = hud.clock.tick(FPS)  # Limit frame rate
            current_time = pygame.time.get_ticks()  # current time in ms
            
            self.handle_events(current_time)
            
            if self.update(current_time):
                self.render()
        
        pygame.quit()
        sys.exit()