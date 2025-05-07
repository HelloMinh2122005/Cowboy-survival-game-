import pygame
import sys
from src.entities.hero import Hero
from src.entities.explosion import Explosion
from src.configs.config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BACKGROUND
import ui.hud as hud
from src.systems.level import LevelManager
from src.systems.collision import CollisionManager

def main():
    # Groups for sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()  

    # Create hero
    hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(hero)
    
    # Initialize level manager
    level_manager = LevelManager()
    level_manager.setup_enemy_timer()
    
    # Initialize collision manager
    collision_manager = CollisionManager(hero, all_sprites, enemies, bullets, explosions, level_manager)
    score = 0
    highest_score = 0

    running = True
    while running:
        dt = hud.clock.tick(FPS)  # Limit frame rate
        current_time = pygame.time.get_ticks()  # current time in ms
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    hero.try_shoot(current_time, bullets)
                    all_sprites.add(bullets)
                elif event.key == pygame.K_p:
                    choice = hud.show_game_pause_popup(hud.screen, collision_manager.score, collision_manager.highest_score)
                    if choice == "exit":
                        running = False
                    else: 
                        pass

            # Spawn enemy event
            if event.type == pygame.USEREVENT + 1:
                if level_manager.remaining_enemies > 0:
                    level_manager.spawn_enemy(enemies, all_sprites)
        
        # Update hero
        hero.handle_movement(keys_pressed)
        hero.update_shooting_cooldown(current_time)

        # Update enemies
        for enemy in enemies:
            enemy.update_shooting_cooldown(current_time)
            enemy.update(hero, bullets, current_time)

        all_sprites.add(bullets)
        
        # Update bullets
        bullets.update()

        # Check collisions and update game state
        game_status = collision_manager.update(hud.screen)
        
        if not game_status["running"]:
            running = False
        
        if game_status["reset"]:
            hero = collision_manager.reset_game()
            continue

        current_time = pygame.time.get_ticks()
        for explosion in explosions:
            explosion.update(current_time)

        hud.screen.blit(BACKGROUND, (0, 0))

        # Draw all sprites
        all_sprites.draw(hud.screen)
        
        hud.display_hud(hud.screen, hero.hp, collision_manager.score, collision_manager.highest_score)
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()