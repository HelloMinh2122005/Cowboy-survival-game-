import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.configs.config import FPS, clock
from src.helpers.font_helper import get_font, FONT_LARGE, FONT_MEDIUM, FONT_SMALL
from src.helpers.font_helper import get_font, FONT_MEDIUM
from moviepy.video.io.VideoFileClip import VideoFileClip

def show_game_image_main_menu(screen):
    # Colors
    WHITE = (255, 255, 255)
    GOLD = (255, 215, 0)  # For title
    GREEN = (0, 200, 0)   # For button
    
    # Load background image
    try:
        background_image = pygame.image.load("assets/images/main_menu_img.png")
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Main menu background loaded successfully")
    except Exception as e:
        print(f"Error loading main menu background: {e}")
        background_image = None
    
    # Create fonts
    font_title = get_font(FONT_LARGE)
    font_button = get_font(FONT_MEDIUM)
    
    # Create title with "bold" effect by rendering twice with slight offset
    title_text1 = font_title.render("Chiến tranh chống Mỹ,", True, GOLD)
    title_text1_shadow = font_title.render("Chiến tranh chống Mỹ,", True, GOLD)
    
    title_text2 = font_title.render("thống nhất đất nước", True, GOLD)
    title_text2_shadow = font_title.render("thống nhất đất nước", True, GOLD)
    
    # Position title (centered horizontally)
    title1_x = (SCREEN_WIDTH - title_text1.get_width()) // 2
    title1_y = 100
    title2_x = (SCREEN_WIDTH - title_text2.get_width()) // 2
    title2_y = 160  # Position below the first line
    
    # Create play button
    play_text = font_button.render("Chơi", True, WHITE)
    button_width = 200
    button_height = 70
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT - 200  # Position button near bottom
    play_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Main menu loop
    menu_running = True
    while menu_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if play button was clicked
                if play_button_rect.collidepoint(mouse_pos):
                    return "play"
        
        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            # Fallback background color if image fails to load
            screen.fill((0, 0, 0))
            
        # Draw title with "bold" effect - shadow first, then main text
        offset = 2  # Adjust this for bold thickness
        
        # Draw shadows first
        screen.blit(title_text1_shadow, (title1_x + offset, title1_y + offset))
        screen.blit(title_text2_shadow, (title2_x + offset, title2_y + offset))
        
        # Draw main text
        screen.blit(title_text1, (title1_x, title1_y))
        screen.blit(title_text2, (title2_x, title2_y))
        
        # Draw play button
        pygame.draw.rect(screen, GREEN, play_button_rect, border_radius=20)
        
        # Draw button text (centered on button)
        play_text_x = button_x + (button_width - play_text.get_width()) // 2
        play_text_y = button_y + (button_height - play_text.get_height()) // 2
        screen.blit(play_text, (play_text_x, play_text_y))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    return "exit"