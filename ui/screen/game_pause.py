import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock

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