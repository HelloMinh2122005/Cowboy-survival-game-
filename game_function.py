import pygame
import random 
from enemy import Enemy 
from configs.config import SCREEN_WIDTH, SCREEN_HEIGHT

from configs.config import FPS, clock, screen

def spawn_enemy(enemy_group):
    """Spawn an enemy at a random edge of the screen."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, SCREEN_WIDTH)
        y = 0
    elif side == "bottom":
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    elif side == "left":
        x = 0
        y = random.randint(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT)
    
    enemy = Enemy(x, y)
    enemy_group.add(enemy)

def show_game_over_popup(screen, current_score, high_score):

    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)

    # Prepare text surfaces
    lose_text = font_big.render("You Lose!", True, WHITE)
    score_text = font_small.render(f"Score: {current_score}", True, WHITE)
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)

    # Button text
    retry_text = font_small.render("Retry", True, WHITE)
    exit_text = font_small.render("Exit", True, WHITE)

    # Create a semi-transparent overlay or a popup rectangle
    popup_width = 400
    popup_height = 300
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Button rectangles (retry and exit)
    button_width = 120
    button_height = 50

    # Retry button
    retry_button_x = popup_x + 50
    retry_button_y = popup_y + 200
    retry_button_rect = pygame.Rect(retry_button_x, retry_button_y, button_width, button_height)

    # Exit button
    exit_button_x = popup_x + 230
    exit_button_y = popup_y + 200
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)

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

        # Darken background
        screen.fill((30, 30, 30))

        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)

        # Draw "You Lose"
        screen.blit(lose_text, (popup_x + 100, popup_y + 30))
        # Draw current score
        screen.blit(score_text, (popup_x + 60, popup_y + 100))
        # Draw high score
        screen.blit(high_score_text, (popup_x + 60, popup_y + 140))

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

def show_game_pause_popup(screen, score, highest_score):
    
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    GREEN = (0, 200, 0)
    BLUE = (0, 100, 200)
    RED = (200, 0, 0)

    # Prepare text surfaces
    pause_text = font_big.render("Game Paused", True, WHITE)
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    high_score_text = font_small.render(f"High Score: {highest_score}", True, WHITE)

    # Button text
    resume_text = font_small.render("Resume", True, WHITE)
    exit_text = font_small.render("Exit", True, WHITE)

    # Create a semi-transparent overlay or a popup rectangle
    popup_width = 400
    popup_height = 300
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Button rectangles
    button_width = 120
    button_height = 50

    # Resume button
    resume_button_x = popup_x + (popup_width - button_width) // 2
    resume_button_y = popup_y + 160
    resume_button_rect = pygame.Rect(resume_button_x, resume_button_y, button_width, button_height)

    # Exit button
    exit_button_x = popup_x + (popup_width - button_width) // 2
    exit_button_y = popup_y + 220
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)

    popup_running = True
    while popup_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"  # Resume on ESC key

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if resume_button_rect.collidepoint(mouse_pos):
                    return "resume"
                if exit_button_rect.collidepoint(mouse_pos):
                    return "exit"

        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha for transparency
        screen.blit(overlay, (0, 0))

        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)

        # Draw title
        screen.blit(pause_text, (popup_x + (popup_width - pause_text.get_width()) // 2, popup_y + 30))
        
        # Draw score and high score
        screen.blit(score_text, (popup_x + 60, popup_y + 90))
        screen.blit(high_score_text, (popup_x + 60, popup_y + 120))

        # Draw buttons
        pygame.draw.rect(screen, GREEN, resume_button_rect)
        pygame.draw.rect(screen, RED, exit_button_rect)

        # Text on buttons
        screen.blit(resume_text,
                    (resume_button_rect.centerx - resume_text.get_width() // 2,
                     resume_button_rect.centery - resume_text.get_height() // 2))
        screen.blit(exit_text,
                    (exit_button_rect.centerx - exit_text.get_width() // 2,
                     exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    return "resume"

def show_game_next_level(screen, level):
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    GREEN = (0, 200, 0)

    # Prepare text surfaces
    level_complete_text = font_big.render(f"Level {level} Complete!", True, WHITE)
    next_level_text = font_small.render(f"Ready for Level {level+1}?", True, WHITE)
    
    # Button text
    next_button_text = font_small.render("Next", True, WHITE)
    
    # Create popup rectangle
    popup_width = 400
    popup_height = 250
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    # Next button
    button_width = 120
    button_height = 50
    next_button_x = popup_x + (popup_width - button_width) // 2
    next_button_y = popup_y + 170
    next_button_rect = pygame.Rect(next_button_x, next_button_y, button_width, button_height)
    
    popup_running = True
    while popup_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if next_button_rect.collidepoint(mouse_pos):
                    return "next"
                    
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha for transparency
        screen.blit(overlay, (0, 0))
        
        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)
        
        # Draw title and text
        screen.blit(level_complete_text, 
                   (popup_x + (popup_width - level_complete_text.get_width()) // 2, 
                    popup_y + 40))
        screen.blit(next_level_text, 
                   (popup_x + (popup_width - next_level_text.get_width()) // 2, 
                    popup_y + 110))
                    
        # Draw next button
        pygame.draw.rect(screen, GREEN, next_button_rect)
        
        # Button text
        screen.blit(next_button_text,
                   (next_button_rect.centerx - next_button_text.get_width() // 2,
                    next_button_rect.centery - next_button_text.get_height() // 2))
                    
        pygame.display.flip()
        clock.tick(FPS)
        
    return "next"

def show_vid_next_level(screen, level):
    vid_to_display = [
        "assets/videos/00.mp4",
        "assets/videos/01.mp4",
        "assets/videos/02.mp4",
        "assets/videos/03.mp4",
        "assets/videos/04.mp4",
    ]