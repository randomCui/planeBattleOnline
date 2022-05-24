import random
import sys

sys.path.append('../base')

from base.enemy import EnemyType1
from base.config import window_width, window_height, setting


def enemy_spawn(game, t):
    ch = random.randint(1, 2)
    temp = None
    if ch == 1:
        t = EnemyType1(
            basic_setting={
                'x': random.randint(0, window_width),
                'y': random.randint(0, window_height),
                'size': t.lib['GREEN_SPACE_SHIP'].get_size(),
                'texture_name': 'GREEN_SPACE_SHIP'
            },
            inertia_setting={
                'max_speed': 2
            },
            plane_setting={
                'health': setting[game.difficult]['enemy_health'][0]
            }
        )
        t.init_move((0, 2))
    game.enemies.append(t)
