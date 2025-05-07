import pygame
from src.configs.difficulty_config import *
import ui.hud as hud
from src.systems.spawner import spawn_enemy

class LevelManager:
    def __init__(self):
        # Level configuration
        self.game_difficulty = [
            [ENEMY_NUM_LV1, ENEMY_SPAWN_INTERVAL_LV1],
            [ENEMY_NUM_LV2, ENEMY_SPAWN_INTERVAL_LV2],
            [ENEMY_NUM_LV3, ENEMY_SPAWN_INTERVAL_LV3],
            [ENEMY_NUM_LV4, ENEMY_SPAWN_INTERVAL_LV4],
            [ENEMY_NUM_LV5, ENEMY_SPAWN_INTERVAL_LV5]
        ]
        
        # Level state
        self.current_level = 0
        self.current_enemy_count = 0
        self.remaining_enemies = self.game_difficulty[self.current_level][0]
        
    def setup_enemy_timer(self):
        """Set up the enemy spawn timer based on current level"""
        pygame.time.set_timer(pygame.USEREVENT + 1, self.game_difficulty[self.current_level][1])
    
    def spawn_enemy(self, enemies, all_sprites):
        """Spawn an enemy and update counters"""
        self.current_enemy_count += 1
        self.remaining_enemies -= 1
        spawn_enemy(enemies)
        all_sprites.add(enemies)
        
    def enemy_killed(self):
        """Called when an enemy is killed"""
        self.current_enemy_count -= 1
        return self.check_level_complete()
        
    def check_level_complete(self):
        """Check if the current level is complete"""
        if self.current_enemy_count <= 0 and self.remaining_enemies <= 0:
            return True
        return False
        
    def advance_level(self, screen):
        """Advance to the next level"""
        self.current_level += 1
        if self.current_level >= len(self.game_difficulty):
            # Game completed - could handle final victory screen here
            return False
            
        self.current_enemy_count = 0
        self.remaining_enemies = self.game_difficulty[self.current_level][0]
        
        # Set up the new timer for enemy spawning
        self.setup_enemy_timer()
        
        # Show level transition screens
        hud.show_vid_next_level(screen, self.current_level)
        hud.show_game_next_level(screen, self.current_level)
        return True
        
    def reset(self):
        """Reset the level manager for a new game"""
        self.current_level = 0
        self.current_enemy_count = 0
        self.remaining_enemies = self.game_difficulty[self.current_level][0]
        self.setup_enemy_timer()