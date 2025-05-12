import random 
from src.entities.enemy import Enemy 
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock, screen
import pygame
from src.helpers.font_helper import get_font
from .screen.game_over import show_game_over_popup
from .screen.game_pause import show_game_pause_popup
from .screen.next_level import show_game_next_level, show_vid_next_level
from .screen.game_win import show_game_win_popup
from .screen.game_main_menu import show_game_image_main_menu

def display_hud(screen, hero_hp, current_level):
    """Display the game HUD with health, score, and highest score"""
    font = get_font(36)
    
    hp_text = font.render(f"HP: {hero_hp}", True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))

    score_text = font.render(f"Màn chơi hiện tại: {current_level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))