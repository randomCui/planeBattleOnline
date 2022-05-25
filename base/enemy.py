from math import pi

from base.bullet import BulletSimple, BulletAiming
from base.missile import Missile
from base.plane import Plane
from shared_lib import t
from util import distance_between, vector_angle_from_y


class Enemy(Plane):
    def __init__(self, **properties):
        # 将参数传递给自己的基类
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        # 开火冷却间隔
        self.fire_cool_down_frame = None
        # 上次开火时间
        self.last_fire = 0
        # 击落一个敌机应得的分数
        self.score = 10

        # 获取本级的属性
        for key, value in properties['enemy_setting'].items():
            setattr(self, key, value)

    def update(self):
        super(Enemy, self).update()

    def hit(self, amount=1):
        super(Enemy, self).hit()

    def init_move(self, speed_vector):
        super(Enemy, self).init_move(speed_vector)

    def shoot(self, **kwargs):
        pass


class EnemyType1(Enemy):
    """
    EnemyType1完全继承Enemy，其发射的子弹是简单向前的子弹
    """
    pass


class EnemyType2(Plane):
    """
    EnemyType2发射瞄准的子弹
    """
    def __init__(self, **properties):
        # 将参数传递给上一级
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        # 开火冷却间隔
        self.fire_cool_down_frame = None
        # 距离上次开火隔了多久
        self.last_fire = 0
        # 击落一架敌机应该获得的分数
        self.score = 30

        # 获取本级的参数
        for key, value in properties['enemy_setting'].items():
            setattr(self, key, value)

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
                    'x': self.get_center()[0] - t.lib['BLUE_LASER'].get_size()[0] / 2,
                    'y': self.get_center()[1] - 30,
                    'size': t.lib['BLUE_LASER'].get_size(),
                    'texture_name': 'BLUE_LASER',
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


class EnemyType3(Enemy):
    """
    EnemyType3发射追踪的导弹
    """
    def __init__(self, **properties):
        # 将参数传递给上一级
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         enemy_setting=properties['enemy_setting'],
                         )
        # 击落一架敌机获得的分数
        self.score = 50

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
            # 同时将这个玩家对象的引用也记录下来，用于导弹之后一直追踪
            target_object = players[min_distance_key]
            # 生成一个导弹
            temp = Missile(
                basic_setting={
                    'x': self.get_center()[0] - t.lib['ENERGY_BALL'].get_size()[0] / 2,
                    'y': self.get_center()[1] + 30,
                    'size': t.lib['ENERGY_BALL'].get_size(),
                    'texture_name': 'ENERGY_BALL',
                },
                inertia_setting={
                    'max_speed': 5,
                },
                missile_setting={
                    'health': 5,
                    'damage': 1,
                    'target': target,
                    'target_object': target_object,
                    'life_time': 150
                },
            )
            # 返回子弹生成成功的标志以及生成的子弹对象
            return True, temp
        else:
            # 如果本次没来得及开火，那么就返回子弹生成失败的标志，将上次开火时间+1
            self.last_fire += 1
            return False, None
