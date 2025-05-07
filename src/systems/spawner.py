import random 
from src.entities.enemy import Enemy 
from src.configs.config import SCREEN_WIDTH, SCREEN_HEIGHT

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