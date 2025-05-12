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
    
    # Create title
    title_text1 = font_title.render("Chiến tranh chống Mỹ,", True, GOLD)
    title_text2 = font_title.render("thống nhất đất nước", True, GOLD)
    
    # Position title (centered horizontally)
    title1_x = (SCREEN_WIDTH - title_text1.get_width()) // 2
    title1_y = 100
    title2_x = (SCREEN_WIDTH - title_text2.get_width()) // 2
    title2_y = 160  # Position below the first line
    
    # Create play button
    play_text = font_button.render("Chơi", False, WHITE)
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
            
        # Draw title
        screen.blit(title_text1, (title1_x, title1_y))
        screen.blit(title_text2, (title2_x, title2_y))
        
        # Draw play button
        pygame.draw.rect(screen, GREEN, play_button_rect)
        
        # Draw button text (centered on button)
        play_text_x = button_x + (button_width - play_text.get_width()) // 2
        play_text_y = button_y + (button_height - play_text.get_height()) // 2
        screen.blit(play_text, (play_text_x, play_text_y))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    return "exit"

def show_vid_intro(screen):
    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)   # For button
    GRAY = (50, 50, 50)
    
    # Video path
    video_path = "assets/videos/Main_Menu.mp4"  
    
    # Load video
    try:
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration
        print(f"Video loaded successfully, duration: {video_duration}s")
        
        # Calculate video dimensions while maintaining aspect ratio
        video_ratio = video_clip.w / video_clip.h
        
        # We'll display the video at full screen size
        video_width = SCREEN_WIDTH
        video_height = int(SCREEN_WIDTH / video_ratio)
        
        # If calculated height is greater than screen height, recalculate
        if video_height > SCREEN_HEIGHT:
            video_height = SCREEN_HEIGHT
            video_width = int(SCREEN_HEIGHT * video_ratio)
        
        is_video_playing = True
    except Exception as e:
        print(f"Error loading video: {e}")
        video_clip = None
        is_video_playing = False
    
    # Create play button
    font_button = get_font(FONT_MEDIUM)
    play_text = font_button.render("Chơi", False, WHITE)
    
    button_width = 200
    button_height = 70
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT - 120  # Position button near bottom
    play_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Video playback variables
    start_time = pygame.time.get_ticks() / 1000  # Current time in seconds
    video_complete = False
    last_frame = None
    
    intro_running = True
    while intro_running:
        current_time = pygame.time.get_ticks() / 1000
        video_time = current_time - start_time
        
        # Mark video as complete when it reaches the end
        if video_clip and is_video_playing and video_time >= video_duration:
            # Capture last frame
            try:
                last_frame = video_clip.get_frame(video_duration - 0.1)  # Get frame just before end
                last_frame_surface = pygame.surfarray.make_surface(last_frame.swapaxes(0, 1))
                last_frame_surface = pygame.transform.scale(last_frame_surface, (video_width, video_height))
            except Exception as e:
                print(f"Error getting last frame: {e}")
                last_frame = None
            
            is_video_playing = False
            video_complete = True
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if video_clip:
                    video_clip.close()
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if play button was clicked
                if play_button_rect.collidepoint(mouse_pos):
                    if video_clip:
                        video_clip.close()
                    return "play"
        
        # Fill screen with black
        screen.fill((0, 0, 0))
        
        # Draw current video frame if playing
        if video_clip and is_video_playing:
            try:
                frame = video_clip.get_frame(video_time)
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                frame_surface = pygame.transform.scale(frame_surface, (video_width, video_height))
                
                # Center the video on screen
                video_x = (SCREEN_WIDTH - video_width) // 2
                video_y = (SCREEN_HEIGHT - video_height) // 2
                
                screen.blit(frame_surface, (video_x, video_y))
            except Exception as e:
                print(f"Error playing video frame at {video_time}: {e}")
                is_video_playing = False
        
        # Draw last frame when video complete
        elif video_complete and last_frame_surface:
            video_x = (SCREEN_WIDTH - video_width) // 2
            video_y = (SCREEN_HEIGHT - video_height) // 2
            screen.blit(last_frame_surface, (video_x, video_y))
        
        # Draw play button
        pygame.draw.rect(screen, GREEN, play_button_rect)
        
        # Draw button text (centered on button)
        play_text_x = button_x + (button_width - play_text.get_width()) // 2
        play_text_y = button_y + (button_height - play_text.get_height()) // 2
        screen.blit(play_text, (play_text_x, play_text_y))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    if video_clip:
        video_clip.close()
    
    return "exit"