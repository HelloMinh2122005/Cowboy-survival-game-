import pygame
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock
from moviepy.video.io.VideoFileClip import VideoFileClip

def show_vid_next_level(screen, level):
    vid_to_display = [
        "assets/videos/00.mp4",
        "assets/videos/01.mp4",
        "assets/videos/02.mp4",
        "assets/videos/03.mp4",
        "assets/videos/04.mp4",
    ]
    
    # Get the video path for the current level
    video_path = vid_to_display[level]
    
    video_max_width = SCREEN_WIDTH // 2
    video_max_height = SCREEN_HEIGHT // 2
    
    # Load video
    video_clip = VideoFileClip(video_path)
    video_duration = video_clip.duration
    
    # Calculate video dimensions while maintaining aspect ratio
    video_ratio = video_clip.w / video_clip.h
    if video_ratio > 1:  # wider than tall
        video_width = video_max_width
        video_height = int(video_max_width / video_ratio)
    else:  # taller than wide
        video_height = video_max_height
        video_width = int(video_max_height * video_ratio)
    
    # Set up UI elements
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    GREEN = (0, 200, 0)
    
    # Prepare text
    level_text = font_big.render(f"Level {level+1}", True, WHITE)
    next_button_text = font_small.render("Next", True, WHITE)
    
    # Create popup rectangle - make it larger to accommodate the video
    popup_width = max(500, video_width + 100)
    popup_height = video_height + 200
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    # Calculate video position (centered in popup)
    video_x = popup_x + (popup_width - video_width) // 2
    video_y = popup_y + 80
    video_rect = pygame.Rect(video_x, video_y, video_width, video_height)
    
    # Next button
    button_width = 120
    button_height = 50
    next_button_x = popup_x + (popup_width - button_width) // 2
    next_button_y = popup_y + popup_height - 70
    next_button_rect = pygame.Rect(next_button_x, next_button_y, button_width, button_height)
    
    # Video playback variables
    start_time = pygame.time.get_ticks() / 1000  # Current time in seconds
    is_video_playing = True
    
    popup_running = True
    while popup_running:
        current_time = pygame.time.get_ticks() / 1000
        video_time = current_time - start_time
        
        # Loop the video if it reaches the end
        if video_time >= video_duration:
            start_time = current_time
            video_time = 0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_clip.close()
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if next_button_rect.collidepoint(mouse_pos):
                    video_clip.close()
                    return "next"
        
        # Create semi-transparent overlay for the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha for transparency
        screen.blit(overlay, (0, 0))
        
        # Draw popup
        pygame.draw.rect(screen, GRAY, popup_rect)
        
        # Draw title
        screen.blit(level_text, 
                  (popup_x + (popup_width - level_text.get_width()) // 2, 
                   popup_y + 20))
        
        # Draw current video frame
        if is_video_playing:
            try:
                frame = video_clip.get_frame(video_time)
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                frame_surface = pygame.transform.scale(frame_surface, (video_width, video_height))
                screen.blit(frame_surface, (video_x, video_y))
            except Exception as e:
                print(f"Error playing video: {e}")
                is_video_playing = False
        
        # Draw video border
        pygame.draw.rect(screen, WHITE, video_rect, 2)
        
        # Draw next button
        pygame.draw.rect(screen, GREEN, next_button_rect)
        
        # Button text
        screen.blit(next_button_text,
                  (next_button_rect.centerx - next_button_text.get_width() // 2,
                   next_button_rect.centery - next_button_text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    video_clip.close()
    return "next"

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
