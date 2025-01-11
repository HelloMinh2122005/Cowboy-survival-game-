import pygame
import sys
from hero import Hero
from bomb import Bomb
import game_function as gf


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

ENEMY_SPAWN_INTERVAL = 2000  # milliseconds (2 seconds)

def main():
    # Groups for sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    # Create hero
    hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(hero)
    
    # Enemy spawn timer
    pygame.time.set_timer(pygame.USEREVENT + 1, ENEMY_SPAWN_INTERVAL)
    
    # Score variables
    score = 0
    high_score = 0

    running = True
    while running:
        dt = gf.clock.tick(FPS)  # Limit frame rate
        current_time = pygame.time.get_ticks()  # current time in ms
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                running = False
            
            # Hero tries to shoot
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hero.try_shoot(current_time, bullets)
                    all_sprites.add(bullets)


            # Hero tries to land bomb
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    bomb = Bomb(hero.rect.centerx, hero.rect.centery, "hero", None)
                    all_sprites.add(bomb)
                    bombs.add(bomb)
            
            # Spawn enemy event
            if event.type == pygame.USEREVENT + 1:
                gf.spawn_enemy(enemies)
                all_sprites.add(enemies)
        
        # Update hero
        hero.handle_movement(keys_pressed)
        hero.update_shooting_cooldown(current_time)
        hero.update_landing_bomb_cooldown(current_time)

        # Update enemies
        for enemy in enemies:
            enemy.update_shooting_cooldown(current_time)
            enemy.update(hero, bullets, current_time)
        
        # Update bullets
        bullets.update()

        current_time = pygame.time.get_ticks()
        for bomb in bombs:
            bomb.update(current_time, all_sprites)
        
        # Check collisions: enemy bullet -> hero
        for bullet in bullets:
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(hero.rect):
                    hero.hp -= 1
                    bullet.destroy()
                    if hero.hp <= 0:
                        print("Game Over! You died.")
                        choice = gf.show_game_over_popup(gf.screen, score, high_score)

                        if choice == "exit":
                            running = False

                        elif choice == "retry":
                            # Re-initialize the game, but keep high_score
                            # 1) Clear all groups
                            all_sprites.empty()
                            enemies.empty()
                            bullets.empty()
                            # 2) Recreate the hero at center
                            hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            all_sprites.add(hero)
                            # 3) Reset score to 0
                            score = 0
                            # 4) Keep the same spawn timer
                            pygame.time.set_timer(pygame.USEREVENT + 1, ENEMY_SPAWN_INTERVAL)
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
                            enemy.kill()
                            # Increase score
                            score += 1
                            if score > high_score:
                                high_score = score
        
        # check collisions: hero bomb -> enemy
        for enemy in enemies:
            for bomb in bombs:
                if bomb.rect.colliderect(enemy.rect):
                    enemy.hp -= 3
                    bomb.destroy()
                    if enemy.hp <= 0:
                        enemy.kill()
                        # Increase score
                        score += 1
                        if score > high_score:
                            high_score = score

        # Clear screen
        gf.screen.fill((30, 30, 30))
        
        # Draw all sprites
        all_sprites.draw(gf.screen)
        
        # Display HUD (HP, Score, High Score)
        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"HP: {hero.hp}", True, (255, 255, 255))
        gf.screen.blit(hp_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        gf.screen.blit(score_text, (10, 50))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        gf.screen.blit(high_score_text, (10, 90))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()