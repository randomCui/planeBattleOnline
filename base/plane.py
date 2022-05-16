from inertia_object import InertiaObject
from bullet import BulletSimple
from shared_lib import t


class Plane(InertiaObject):
    def __init__(self, **properties):
        """
        初始化玩家对象

        :param x: 初始时对象的x位置
        :param y: 初始时对象的y位置
        :param width: 初始时对象的宽度
        :param height: 初始时对象的高度
        :param properties: 其余玩家对象需要的各种属性，例如生命值，技能量等
        """
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         )

        self.health = None
        self.last_fire = 0

        for key, value in properties['plane_setting'].items():
            setattr(self, key, value)

    def hit(self, amount=1):
        assert self.health is not None
        self.health -= amount

    def init_move(self, speed_vector):
        self.vx, self.vy = speed_vector

    def shoot(self, **kwargs):
        assert self.fire_cool_down_frame is not None
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0
            temp = BulletSimple(
                basic_setting={
                    'x': self.get_center()[0] - t.lib['BLUE_LASER'].get_size()[0] / 2,
                    'y': self.get_center()[1] - t.lib['BLUE_LASER'].get_size()[1] / 2,
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
            temp.init_shoot_move((0, 0))
            return True, temp
        else:
            self.last_fire += 1
            return False, None
