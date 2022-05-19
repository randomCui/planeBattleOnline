from bullet import BulletAiming
from plane import Plane
import time
import random
from base.config import window_height as height
from base.config import window_width as width
from base.util import vector_from_A_to_B, distance_between, vector_angle_from_y
from base.shared_lib import t


class BossType1(Plane):
    def __init__(self, **kwargs):
        super().__init__(basic_setting=kwargs['basic_setting'],
                         inertia_setting=kwargs['inertia_setting'],
                         plane_setting=kwargs['plane_setting'],
                         )
        self.angle = 0

        self.random_gen = random.Random()
        self.random_gen.seed(time.time())

        self.change_interest = 120
        self.interest_place = None

        self.frame_past = 0
        self.timer = time.time()

        self.fire_cool_down_frame = None
        self.last_fire = 0

        for key, value in kwargs['boss_setting'].items():
            setattr(self, key, value)

    def update(self):
        if self.frame_past % self.change_interest == 0:
            self.go_to_elsewhere()
        self.change_pos(
            vector_from_A_to_B(self.get_pos(),self.interest_place)
        )
        self.frame_past += 1
        super().update()


    def go_to_elsewhere(self):
        self.interest_place = (
            self.random_gen.randint(0, width),
            self.random_gen.randint(0, height//4),
        )

    def shoot(self, players):
        assert self.fire_cool_down_frame is not None
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0

            # 选择要攻击哪一个玩家
            min_distance_key = ''
            min_distance_value = 1E6
            for key, value in players.items():
                if min_distance_value > distance_between(value.get_center(), self.get_center()):
                    min_distance_value = distance_between(value.get_center(), self.get_center())
                    min_distance_key = key

            target = players[min_distance_key].get_center()
            target_vector = target[0] - self.get_center()[0], target[1] - self.get_center()[1]
            angle_from_y = vector_angle_from_y(target_vector)

            # 如果已经超过攻击角度，就放弃攻击
            if abs(angle_from_y) > 60 or self.y > target[1]:
                return False, None

            temp = BulletAiming(
                basic_setting={
                    'x': self.get_center()[0] - t.lib['YELLOW_LASER'].get_size()[0] / 2,
                    'y': self.get_center()[1] - 30,
                    'size': t.lib['YELLOW_LASER'].get_size(),
                    'texture_name': 'YELLOW_LASER',
                },
                inertia_setting={
                    'max_speed': 5,
                },
                bullet_setting={
                    'damage': 1,
                    'target': target,
                    'angle': angle_from_y,
                },
            )
            return True, temp
        else:
            self.last_fire += 1
            return False, None

    def attack(self):
        pass

