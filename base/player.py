from plane import Plane
from bullet import BulletSimple
from shared_lib import t


class Player(Plane):
    def __init__(self, **properties):
        self.fire_cool_down_frame = None
        self.want_to_shoot = False
        self.nickname = ''
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
                         plane_setting=properties['plane_setting'],
                         )
        for key, value in properties['player_setting'].items():
            setattr(self, key, value)

    def shoot(self, **kwargs):
        if self.want_to_shoot:
            self.want_to_shoot = False
            assert self.fire_cool_down_frame is not None
            if self.last_fire > self.fire_cool_down_frame:
                self.last_fire = 0
                temp = BulletSimple(
                    basic_setting={
                        'x': self.get_center()[0] - t.lib['RED_LASER'].get_size()[0] / 2,
                        'y': self.get_center()[1] - t.lib['RED_LASER'].get_size()[1] / 2,
                        'size': t.lib['RED_LASER'].get_size(),
                        'texture_name': 'RED_LASER',
                    },
                    inertia_setting={
                        'max_speed': 5,
                    },
                    bullet_setting={
                        'damage': 4,
                    },
                )
                temp.init_shoot_move((0, -5))
                return True, temp

        self.last_fire += 1

        return False, None

