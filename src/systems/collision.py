import pygame
from src.entities.explosion import Explosion
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.hero import Hero
import ui.hud as hud

class CollisionManager:
    def __init__(self, hero, all_sprites, enemies, bullets, explosions, level_manager):
        self.hero = hero
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.bullets = bullets
        self.explosions = explosions
        self.level_manager = level_manager

    def check_enemy_bullets_hero_collision(self, screen):
        """Check collisions between enemy bullets and hero"""
        game_status = {"running": True, "reset": False}
        
        for bullet in self.bullets:
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(self.hero.rect):
                    self.hero.hp -= 1
                    bullet.destroy()
                    if self.hero.hp <= 0:
                        print("Game Over! You died.")
                        choice = hud.show_game_over_popup(screen)

                        if choice == "exit":
                            game_status["running"] = False
                        elif choice == "retry":
                            game_status["reset"] = True
        
        return game_status

    def check_hero_bullets_enemy_collision(self, screen):
        """Check collisions between hero bullets and enemies"""
        game_status = {"running": True, "reset": False}  # Initialize game_status
        
        for enemy in self.enemies:
            for bullet in self.bullets:
                if bullet.owner == "hero":
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= 1
                        bullet.destroy()
                        if enemy.hp <= 0:
                            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                            self.explosions.add(explosion)
                            self.all_sprites.add(explosion)
                            enemy.kill()
                            
                            # Check if level is complete
                            if self.level_manager.enemy_killed():
                                level_result, choice = self.level_manager.advance_level(screen)
                                if choice == "exit":
                                    game_status["running"] = False
                                elif choice == "retry":
                                    game_status["reset"] = True
        
        return game_status 

    def reset_game(self):
        """Reset the game state while keeping highest score"""
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.hero = Hero(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.hero)
        self.level_manager.reset()
        return self.hero
        
    def update(self, screen):
        """Run all collision checks and update game state"""
        game_status1 = self.check_enemy_bullets_hero_collision(screen)
        game_status2 = self.check_hero_bullets_enemy_collision(screen)
        
        # Combine the game status results
        final_status = {
            "running": game_status1["running"] and game_status2["running"],
            "reset": game_status1["reset"] or game_status2.get("reset", False)
        }
        
        return final_status