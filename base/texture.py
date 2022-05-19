import os
import pygame, pygame_menu
from config import window_width as width
from config import window_height as height


class Texture:
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
            'BOSS_1': pygame.image.load(os.path.join("..", "assets", "boss.png")),
        }
        self.menu = {
            'YELLOW_SPACE_SHIP': pygame_menu.BaseImage(
                image_path=os.path.join("..", "assets", "pixel_ship_yellow.png")
            ),
            'BLUE_SPACE_SHIP': pygame_menu.BaseImage(
                image_path=os.path.join("..", "assets", "pixel_ship_blue_small.png")
            ),
        }
