import sys, time, random
sys.path.append('../base')

from base.config import setting,window_height,window_width
from base.enemy import EnemyType1,EnemyType2
from base.texture import Texture
from base.player import Player

t = Texture()


class Game:
    def __init__(self,game_id,difficulty='easy'):
        self.game_id = game_id
        self.enemies = []
        self.players = {}
        self.bullets = []
        self.props = []
        self.running_state = False
        self.difficult = difficulty
        self.start_time = time.time()
        print(self.start_time)
        print(setting[self.difficult]['enemy_spawn_time'])
        self.current_time = self.start_time
        self.timer = {
            'enemy_spawn': 0
        }
        self.random = random.Random()
        self.random.seed(self.current_time)

    def enemy_spawn(self, pos=(0,0), enemy_type=1):
        global t

        # 随机生成一个敌机种类
        # enemy_type = self.random.randint(1,2)
        pos = self.random.randint(0, window_width-100), 30

        if self.timer['enemy_spawn'] > setting[self.difficult]['enemy_spawn_time']:
            # ch = random.randint(1, 2)
            temp = None
            if enemy_type == 1:
                temp = EnemyType1(
                    basic_setting={
                        'x': pos[0],
                        'y': pos[1],
                        'size': t.lib['GREEN_SPACE_SHIP'].get_size(),
                        'texture_name': 'GREEN_SPACE_SHIP'
                    },
                    inertia_setting={
                        'max_speed': 2
                    },
                    plane_setting={
                        'health': setting[self.difficult]['enemy_health']['enemy_1']
                    },
                    enemy_setting={

                    }
                )
                temp.init_move((0, 2))
            self.enemies.append(temp)
            self.timer['enemy_spawn'] = 0

    def update_timer(self):
        # 推算自从上次update以来经过的时间，并更新所有寄存器的值
        time_past = time.time() - self.current_time
        self.current_time = time.time()
        for key, value in self.timer.items():
            self.timer[key] += time_past

    def enemy_move(self):
        for enemy in self.enemies:
            enemy.update()

    def ouf_of_boarder_handler(self):
        for enemy in self.enemies:
            # 说明已经飞出屏幕
            if enemy.get_center()[1] > window_height+100:
                self.enemies.remove(enemy)

    def collision_detection(self):
        pass

    def update(self):
        self.update_timer()
        self.enemy_spawn()
        self.enemy_move()
        self.ouf_of_boarder_handler()

