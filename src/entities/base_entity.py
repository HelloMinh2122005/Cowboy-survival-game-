import pygame

class BaseEntity(pygame.sprite.Sprite):
    """Base class for all game entities."""
    
    def __init__(self, x, y, image_path=None, size=None):
        """
        Initialize a base entity.
        
        Args:
            x (int): X position
            y (int): Y position
            image_path (str, optional): Path to entity image
            size (tuple, optional): Size to scale image (width, height)
        """
        super().__init__()
        
        # Initialize image and rect
        if image_path:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            if size:
                self.original_image = pygame.transform.scale(self.original_image, size)
            self.image = self.original_image
        else:
            # Create a default surface if no image provided
            self.original_image = None
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 255, 255))  # White by default
            
        self.rect = self.image.get_rect(center=(x, y))
        
        # Common attributes
        self.hp = 1
        self.speed = 0
        
        # Shooting attributes (for entities that can shoot)
        self.can_shoot = False
        self.bullet_in_flight = False
        self.next_shot_time = 0
    
    def update(self, *args, **kwargs):
        """Base update method to be overridden by subclasses."""
        pass
    
    def rotate_image(self, angle):
        """
        Rotate the entity image.
        
        Args:
            angle (float): Angle to rotate in degrees
        """
        if self.original_image:
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def update_shooting_cooldown(self, current_time):
        """
        Update shooting cooldown based on current time.
        
        Args:
            current_time (int): Current game time in milliseconds
        """
        if current_time >= self.next_shot_time:
            self.can_shoot = True
    
    def destroy(self):
        """Remove the entity from all sprite groups."""
        self.kill()