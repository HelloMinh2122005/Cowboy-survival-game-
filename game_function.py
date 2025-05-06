import pygame
import random 
from enemy import Enemy 

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
FPS = 60

pygame.init()
pygame.display.set_caption("Dodging Game with Popup")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

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
    """
    Displays a popup that says "You Lose" with the current/ high score, and has 2 buttons:
      - Retry
      - Exit

    Returns "retry" if the user clicks the Retry button,
    Returns "exit" if the user clicks the Exit button,
    or if user closes the window, also return "exit".
    """

    # Fonts and colors
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