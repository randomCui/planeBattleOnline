import random
import time

from base.config import window_height as height
from base.config import window_width as width
from base.shared_lib import t
from base.util import vector_from_A_to_B, distance_between, vector_angle_from_y
from bullet import BulletAiming
from plane import Plane


class BossType1(Plane):
    def __init__(self, **kwargs):
        super().__init__(basic_setting=kwargs['basic_setting'],
                         inertia_setting=kwargs['inertia_setting'],
                         plane_setting=kwargs['plane_setting'],
                         )
        # boss自身的转动角度
        self.angle = 0
        # boss自带的随机数生成器
        self.random_gen = random.Random()
        self.random_gen.seed(time.time())
        # Boss改变自己坐标的频率
        self.change_interest = 120
        # Boss想要前往的点
        self.interest_place = None
        # Boss生成后经过的帧数
        self.frame_past = 0
        # Boss生成时的时间戳
        self.timer = time.time()

        # 射击冷却时间
        self.fire_cool_down_frame = None
        # 上次开火间隔
        self.last_fire = 0

        # 击杀Boss奖励
        self.score = 150

        # 将自身参数填入类内
        for key, value in kwargs['boss_setting'].items():
            setattr(self, key, value)

    def update(self):
        # 如果到了改变目标的时间
        if self.frame_past % self.change_interest == 0:
            # 将让Boss前往其他地方
            self.go_to_elsewhere()
        # 计算从当前点到目标点的向量，并且改变Boss运动状态
        self.change_pos(
            vector_from_A_to_B(self.get_pos(), self.interest_place)
        )
        self.frame_past += 1
        # 更新位置
        super().update()

    def go_to_elsewhere(self):
        # 重新生成一个目标点
        self.interest_place = (
            self.random_gen.randint(0, width),
            self.random_gen.randint(0, height // 4),
        )

    def shoot(self, players):
        # 假设已经设置了开火冷却时间
        assert self.fire_cool_down_frame is not None
        # 如果上次开火时间已经超过了冷却时间
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0
            # 查找最近的玩家
            min_distance_key = ''
            min_distance_value = 1E6
            for key, value in players.items():
                if min_distance_value > distance_between(value.get_center(), self.get_center()):
                    min_distance_value = distance_between(value.get_center(), self.get_center())
                    min_distance_key = key

            # 查找到最近的玩家，将其当前坐标设置为target
            target = players[min_distance_key].get_center()
            target_vector = target[0] - self.get_center()[0], target[1] - self.get_center()[1]
            # 查找到最近的玩家，计算发射角度
            angle_from_y = vector_angle_from_y(target_vector)

            # 如果已经超过攻击角度，就放弃攻击
            if abs(angle_from_y) > 60 or self.y > target[1]:
                return False, None

            # 生成子弹
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
            # 返回子弹生成成功的标志以及生成的子弹对象
            return True, temp
        else:
            # 如果本次没来得及开火，那么就返回子弹生成失败的标志，将上次开火时间+1
            self.last_fire += 1
            return False, None

    def attack(self):
        pass
