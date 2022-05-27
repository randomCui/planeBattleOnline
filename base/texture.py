import os

import pygame
import pygame_menu

from config import window_height as height
from config import window_width as width


class Texture:
    """
    保存了所有的游戏贴图
    """

    def __init__(self):
        # Load images
        self.lib = {
            'RED_SPACE_SHIP': pygame.image.load(os.path.join("..", "assets", "pixel_ship_red_small.png")),
            'GREEN_SPACE_SHIP': pygame.image.load(os.path.join("..", "assets", "pixel_ship_green_small.png")),
            'BLUE_SPACE_SHIP': pygame.image.load(os.path.join("..", "assets", "pixel_ship_blue_small.png")),
            'YELLOW_SPACE_SHIP': pygame.image.load(os.path.join("..", "assets", "pixel_ship_yellow.png")),
            'RED_LASER': pygame.image.load(os.path.join("..", "assets", "pixel_laser_red.png")),
            'GREEN_LASER': pygame.image.load(os.path.join("..", "assets", "pixel_laser_green.png")),
            'BLUE_LASER': pygame.image.load(os.path.join("..", "assets", "pixel_laser_blue.png")),
            'YELLOW_LASER': pygame.image.load(os.path.join("..", "assets", "pixel_laser_yellow.png")),
            'BG': pygame.transform.scale(pygame.image.load(os.path.join("..", "assets", "background-black.png")),
                                         (width, height)
                                         ),
            'ENERGY_BALL': pygame.image.load(os.path.join("..", "assets", "energy_ball.png")),
            'BOSS_1': pygame.image.load(os.path.join("..", "assets", "boss_1.png")),
            'HEALTH_UP': pygame.image.load(os.path.join("..", "assets", "HEALTH_UP.png")),
            'BULLET_UP': pygame.image.load(os.path.join("..", "assets", "tool_kit.png")),
            'SHOOTING_SPEED_UP': pygame.image.load(os.path.join("..", "assets", "tool_kit.png")),
        }
        self.menu = {
            'YELLOW_SPACE_SHIP': pygame_menu.BaseImage(
                image_path=os.path.join("..", "assets", "pixel_ship_yellow.png")
            ),
            'BLUE_SPACE_SHIP': pygame_menu.BaseImage(
                image_path=os.path.join("..", "assets", "pixel_ship_blue_small.png")
            ),
        }
