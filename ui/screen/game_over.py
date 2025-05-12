import pygame
import os
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.configs.config import FPS, clock
from src.helpers.font_helper import get_font, FONT_LARGE, FONT_SMALL

def show_game_over_popup(screen):
    font_big = get_font(FONT_LARGE)
    font_small = get_font(FONT_SMALL)

    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)

    popup_width = 800
    popup_height = 300
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2

    lose_text = font_big.render("Bạn đã hy sinh!", False, WHITE)
    lose_text_x = popup_x + (popup_width - lose_text.get_width()) // 2
    lose_text_y = popup_y + 30

    retry_text = font_small.render("Chơi lại", False, WHITE)
    exit_text = font_small.render("Thoát", False, WHITE)

    
    
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Button dimensions with margins
    button_width = 200
    button_height = 50
    button_margin = 50  
    total_buttons_width = (button_width * 2) + button_margin

    # Center buttons horizontally
    buttons_start_x = popup_x + (popup_width - total_buttons_width) // 2
    buttons_y = popup_y + 200  # Vertical position

    # Retry button
    retry_button_x = buttons_start_x
    retry_button_y = buttons_y
    retry_button_rect = pygame.Rect(retry_button_x, retry_button_y, button_width, button_height)

    # Exit button
    exit_button_x = buttons_start_x + button_width + button_margin
    exit_button_y = buttons_y
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)

    # Load background
    try:
        background_image = pygame.image.load("assets/images/hy_sinh.jpg")
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Error loading background image: {e}")
        background_image = None

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  

    popup_running = True
    while popup_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if user clicked Retry
                if retry_button_rect.collidepoint(mouse_pos):
                    return "retry"

                # Check if user clicked Exit
                if exit_button_rect.collidepoint(mouse_pos):
                    return "exit"
                
        # Draw background image first
        if background_image:
            screen.blit(background_image, (0, 0))
        
        # Apply darkening overlay
        screen.blit(overlay, (0, 0))
        
        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)

        # Draw "You Lose"
        screen.blit(lose_text, (lose_text_x, lose_text_y))
        
        # Draw buttons
        pygame.draw.rect(screen, GREEN, retry_button_rect)
        pygame.draw.rect(screen, RED, exit_button_rect)

        # Text on buttons
        screen.blit(retry_text,
                    (retry_button_rect.centerx - retry_text.get_width() // 2,
                     retry_button_rect.centery - retry_text.get_height() // 2))
        screen.blit(exit_text,
                    (exit_button_rect.centerx - exit_text.get_width() // 2,
                     exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    return "exit"