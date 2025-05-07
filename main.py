import pygame
import sys
from hero import Hero
from explosion import Explosion
import game_function as gf
from configs.config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BACKGROUND
from configs.difficulty_config import *

game_difficulty = [
    [ENEMY_NUM_LV1, ENEMY_SPAWN_INTERVAL_LV1],
    [ENEMY_NUM_LV2, ENEMY_SPAWN_INTERVAL_LV2],
    [ENEMY_NUM_LV3, ENEMY_SPAWN_INTERVAL_LV3],
    [ENEMY_NUM_LV4, ENEMY_SPAWN_INTERVAL_LV4],
    [ENEMY_NUM_LV5, ENEMY_SPAWN_INTERVAL_LV5]
]

def main():
    # Groups for sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()  

    # Create hero
    hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(hero)
    
    # Enemy spawn timer
    current_level = 0
    current_enemy = 0
    pygame.time.set_timer(pygame.USEREVENT + 1, game_difficulty[current_level][1])
    
    # Score variables
    score = 0
    highest_score = 0

    running = True
    while running:
        dt = gf.clock.tick(FPS)  # Limit frame rate
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
                    choice = gf.show_game_pause_popup(gf.screen, score, highest_score)
                    if choice == "exit":
                        running = False
                    else: 
                        pass

            # Spawn enemy event
            if event.type == pygame.USEREVENT + 1:
                current_enemy += 1
                game_difficulty[current_level][0] -= 1
                if game_difficulty[current_level][0] <= 0:
                    pass
                    # wait for next level or game over
                gf.spawn_enemy(enemies)
                all_sprites.add(enemies)
        
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

        current_time = pygame.time.get_ticks()
        
        # Check collisions: enemy bullet -> hero
        for bullet in bullets:
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(hero.rect):
                    hero.hp -= 1
                    bullet.destroy()
                    if hero.hp <= 0:
                        print("Game Over! You died.")
                        choice = gf.show_game_over_popup(gf.screen, score, highest_score)

                        if choice == "exit":
                            running = False

                        elif choice == "retry":
                            # Re-initialize the game, but keep highest_score
                            # 1) Clear all groups
                            all_sprites.empty()
                            enemies.empty()
                            bullets.empty()
                            # 2) Recreate the hero at center
                            hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            all_sprites.add(hero)
                            # 3) Reset score to 0
                            score = 0
                            # 4) Reset level
                            current_level = 0
                            pygame.time.set_timer(pygame.USEREVENT + 1, game_difficulty[current_level][1])
                            # 5) Continue the game loop (i.e. start fresh)
                            continue
        
        # Check collisions: hero bullet -> enemy
        for enemy in enemies:
            for bullet in bullets:
                if bullet.owner == "hero":
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= 1
                        bullet.destroy()
                        if enemy.hp <= 0:
                            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                            explosions.add(explosion)
                            all_sprites.add(explosion)
                            enemy.kill()
                            # Increase score
                            score += 1
                            if score > highest_score:
                                highest_score = score

                            current_enemy -= 1
                            if current_enemy <= 0 and game_difficulty[current_level][0] <= 0: 
                                current_level += 1
                                # show next level here
                                pygame.time.set_timer(pygame.USEREVENT + 1, game_difficulty[current_level][1])
                                gf.show_game_next_level(gf.screen, current_level)
                            

        current_time = pygame.time.get_ticks()
        for explosion in explosions:
            explosion.update(current_time)

        gf.screen.blit(BACKGROUND, (0, 0))

        # Draw all sprites
        all_sprites.draw(gf.screen)
        
        # Display HUD (HP, Score, High Score)
        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"HP: {hero.hp}", True, (255, 255, 255))
        gf.screen.blit(hp_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        gf.screen.blit(score_text, (10, 50))

        highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
        gf.screen.blit(highest_score_text, (10, 90))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()