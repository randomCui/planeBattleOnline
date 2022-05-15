from plane import Plane
from bullet import BulletSimple,BulletAiming
from shared_lib import t
from util import distance_between,vector_angle_from_y
from math import pi


class EnemyType(Plane):
    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        self.fire_cool_down_frame = None
        self.last_fire = 0

        for key, value in properties['enemy_setting'].items():
            setattr(self, key, value)

    def update(self):
        super(EnemyType, self).update()

    def hit(self, amount=1):
        super(EnemyType, self).hit()

    def init_move(self, speed_vector):
        super(EnemyType, self).init_move(speed_vector)

    def shoot(self, **kwargs):
        assert self.fire_cool_down_frame is not None
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0
            temp = BulletSimple(
                basic_setting={
                    'x': self.get_center()[0]-t.lib['BLUE_LASER'].get_size()[0]/2,
                    'y': self.get_center()[1]-t.lib['BLUE_LASER'].get_size()[1]/2,
                    'size': t.lib['BLUE_LASER'].get_size(),
                    'texture_name': 'BLUE_LASER',
                },
                inertia_setting={
                    'max_speed': 5,
                },
                bullet_setting={
                    'damage': 4,
                },
            )
            temp.init_shoot_move((0, 5))
            return True, temp
        else:
            self.last_fire += 1
            return False, None


class EnemyType1(EnemyType):
    pass


class EnemyType2(Plane):
    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        self.fire_cool_down_frame = None
        self.last_fire = 0

        for key, value in properties['enemy_setting'].items():
            setattr(self, key, value)

    def shoot(self, players):
        assert self.fire_cool_down_frame is not None
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0

            # 选择要攻击哪一个玩家
            min_distance_key = ''
            min_distance_value = 1E6
            for key, value in players.items():
                if min_distance_value > distance_between(value.get_center(),self.get_center()):
                    min_distance_value = distance_between(value.get_center(),self.get_center())
                    min_distance_key = key

            target = players[min_distance_key].get_center()
            target_vector = target[0]-self.get_center()[0], target[1]-self.get_center()[1]
            angle_from_y = vector_angle_from_y(target_vector)

            # 如果已经超过攻击角度，就放弃攻击
            if abs(angle_from_y) > pi/4 or self.y > target[1]:
                return False, None

            temp = BulletAiming(
                basic_setting={
                    'x': self.get_center()[0]-t.lib['BLUE_LASER'].get_size()[0]/2,
                    'y': self.get_center()[1]-t.lib['BLUE_LASER'].get_size()[1]/2,
                    'size': t.lib['BLUE_LASER'].get_size(),
                    'texture_name': 'BLUE_LASER',
                },
                inertia_setting={
                    'max_speed': 5,
                },
                bullet_setting={
                    'damage': 1,
                    'target': target,

                },
            )
            return True, temp
        else:
            self.last_fire += 1
            return False, None

