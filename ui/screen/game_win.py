import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock

def show_game_win_popup(screen):
    font_big = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    GOLD = (255, 215, 0)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)  # Added green color for restart button

    # Load victory image
    try:
        victory_image = pygame.image.load("assets/images/win.jpg")
        # Scale image to fit in popup (adjust size as needed)
        image_width = 300
        image_height = 150
        victory_image = pygame.transform.scale(victory_image, (image_width, image_height))
    except Exception as e:
        print(f"Error loading victory image: {e}")
        victory_image = None

    # Prepare text surfaces
    win_text = font_big.render("30/4/1975", True, GOLD)
    congrats_text = font_medium.render("Miền Nam hoàn toàn giải phóng", True, WHITE)

    # Button text
    restart_text = font_small.render("Restart", True, WHITE)
    exit_text = font_small.render("Exit", True, WHITE)

    # Create popup rectangle
    popup_width = 500
    popup_height = 400
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Button rectangles
    button_width = 180
    button_height = 60
    button_spacing = 20  # Space between buttons

    # Position the buttons side by side
    restart_button_x = popup_x + (popup_width // 2) - button_width - (button_spacing // 2)
    exit_button_x = popup_x + (popup_width // 2) + (button_spacing // 2)
    buttons_y = popup_y + popup_height - 100
    
    restart_button_rect = pygame.Rect(restart_button_x, buttons_y, button_width, button_height)
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

        # Create semi-transparent background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha for transparency
        screen.blit(overlay, (0, 0))

        # Draw popup background
        pygame.draw.rect(screen, GRAY, popup_rect)
        
        # Draw gold border around popup
        pygame.draw.rect(screen, GOLD, popup_rect, 4)

        # Draw victory image
        if victory_image:
            image_x = popup_x + (popup_width - image_width) // 2
            image_y = popup_y + 40
            screen.blit(victory_image, (image_x, image_y))
            # Adjust title position to appear below the image
            title_y = image_y + image_height + 10
        else:
            title_y = popup_y + 40

        # Draw title
        screen.blit(win_text, (popup_x + (popup_width - win_text.get_width()) // 2, title_y))
        screen.blit(congrats_text, (popup_x + (popup_width - congrats_text.get_width()) // 2, title_y + 60))
        
        # Draw restart button
        pygame.draw.rect(screen, GREEN, restart_button_rect)
        
        # Draw exit button
        pygame.draw.rect(screen, RED, exit_button_rect)

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