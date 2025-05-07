import random 
from src.entities.enemy import Enemy 
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, screen
import pygame
from .screen.game_over import show_game_over_popup
from .screen.game_pause import show_game_pause_popup
from .screen.next_level import show_game_next_level, show_vid_next_level

def display_hud(screen, hero_hp, score, highest_score):
    """Display the game HUD with health, score, and highest score"""
    font = pygame.font.SysFont(None, 36)
    
    hp_text = font.render(f"HP: {hero_hp}", True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
    screen.blit(highest_score_text, (10, 90))