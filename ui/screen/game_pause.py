import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock
from src.helpers.font_helper import get_font, FONT_LARGE, FONT_SMALL, FONT_MEDIUM


def show_game_pause_popup(screen):
    
    # Load and scale the background to fit the screen
    background = pygame.image.load("assets/images/background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create semi-transparent overlay once (outside the loop)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    
    # Load the image
    try:
        pause_image = pygame.image.load("assets/images/hy_sinh.png")
        image_max_width = SCREEN_WIDTH // 2
        image_max_height = SCREEN_HEIGHT // 2
        
        # Calculate image dimensions while maintaining aspect ratio
        image_ratio = pause_image.get_width() / pause_image.get_height()
        if image_ratio > 1:  # wider than tall
            image_width = image_max_width
            image_height = int(image_max_width / image_ratio)
        else:  # taller than wide
            image_height = image_max_height
            image_width = int(image_max_height * image_ratio)
            
        pause_image = pygame.transform.scale(pause_image, (image_width, image_height))
    except Exception as e:
        print(f"Error loading pause image: {e}")
        image_width = SCREEN_WIDTH // 3
        image_height = SCREEN_HEIGHT // 3
        pause_image = None
    
    font_big = get_font(FONT_LARGE)
    font_small = get_font(FONT_SMALL)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)

    # Prepare text surfaces
    pause_text = font_big.render("Dừng trò chơi", True, WHITE)

    # Button text
    resume_text = font_small.render("Tiếp tục", True, WHITE)
    exit_text = font_small.render("Thoát", True, WHITE)

    # Create a popup rectangle - make it larger to accommodate the image
    popup_width = max(500, image_width + 100)
    popup_height = 250
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    # Calculate image position (centered in popup)
    image_x = popup_x + (popup_width - image_width) // 2
    image_y = popup_y + 80
    image_rect = pygame.Rect(image_x, image_y, image_width, image_height)

    # Button rectangles
    button_width = 150
    button_height = 50

    # Resume button
    resume_button_x = popup_x + popup_width // 4 - button_width // 2
    resume_button_y = popup_y + popup_height - 70
    resume_button_rect = pygame.Rect(resume_button_x, resume_button_y, button_width, button_height)

    # Exit button
    exit_button_x = popup_x + (popup_width * 3) // 4 - button_width // 2
    exit_button_y = popup_y + popup_height - 70
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

        # Draw background and overlay
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)

        # Draw title
        screen.blit(pause_text, (popup_x + (popup_width - pause_text.get_width()) // 2, popup_y + 20))
        
        # Draw image
        if pause_image:
            screen.blit(pause_image, (image_x, image_y))
            # Draw image border
            pygame.draw.rect(screen, WHITE, image_rect, 2)
        
        # Draw buttons
        pygame.draw.rect(screen, GREEN, resume_button_rect, border_radius=20)
        pygame.draw.rect(screen, RED, exit_button_rect, border_radius=20)

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