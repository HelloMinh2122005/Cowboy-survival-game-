import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock
from src.helpers.font_helper import get_font, FONT_LARGE, FONT_SMALL, FONT_MEDIUM


def show_game_win_popup(screen):
    font_small = get_font(FONT_SMALL)
    
    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)

    # Load background image
    try:
        background_image = pygame.image.load("assets/images/final.png")
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Loaded victory background image")
    except Exception as e:
        print(f"Error loading victory background image: {e}")
        background_image = None

    # Button text
    restart_text = font_small.render("Chơi lại", True, WHITE)
    exit_text = font_small.render("Thoát", True, WHITE)

    # Button dimensions
    button_width = 200
    button_height = 70
    button_spacing = 50  # Space between buttons

    # Position the buttons at the bottom of the screen
    buttons_y = SCREEN_HEIGHT - 100
    
    # Restart button (left)
    restart_button_x = (SCREEN_WIDTH // 2) - button_width - (button_spacing // 2)
    restart_button_rect = pygame.Rect(restart_button_x, buttons_y, button_width, button_height)
    
    # Exit button (right)
    exit_button_x = (SCREEN_WIDTH // 2) + (button_spacing // 2)
    exit_button_rect = pygame.Rect(exit_button_x, buttons_y, button_width, button_height)

    popup_running = True
    while popup_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check button clicks
                if exit_button_rect.collidepoint(mouse_pos):
                    return "exit"
                if restart_button_rect.collidepoint(mouse_pos):
                    return "retry"  # Return "retry" for consistency with other screens

        # Draw background image
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            # Fallback if image fails to load
            screen.fill((0, 0, 0))
        
        # Draw restart button
        pygame.draw.rect(screen, GREEN, restart_button_rect, border_radius=20)
        
        # Draw exit button
        pygame.draw.rect(screen, RED, exit_button_rect, border_radius=20)

        # Draw button text
        screen.blit(restart_text,
                  (restart_button_rect.centerx - restart_text.get_width() // 2,
                   restart_button_rect.centery - restart_text.get_height() // 2))
                   
        screen.blit(exit_text,
                  (exit_button_rect.centerx - exit_text.get_width() // 2,
                   exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    return "exit"