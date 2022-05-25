from base.bullet import BulletSimple
from base.defense_laser import DefenseLaser
from base.plane import Plane
from shared_lib import t


class Player(Plane):
    def __init__(self, **properties):
        # 玩家对象的开火冷却帧
        self.fire_cool_down_frame = None
        # 玩家目前是否希望射击
        self.want_to_shoot = False
        # 玩家的昵称
        self.nickname = ''
        # 玩家射出子弹的伤害
        self.damage = 1
        # 玩家射击伤害的因子
        self.damage_factor = 1
        # 玩家的得分
        self.game_score = 0
        # 玩家目前的状态
        self.state = 'alive'

        # 每个玩家对象上的防卫激光数量
        self.defense_laser = []

        # 将参数继续传向基类
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        # 玩家对象需要将生命值条绘制在对象下方，需要重新设置y轴的偏移量
        self._health_bar_y_offset = self.height + 10

        # 将传入的参数设置进类中
        for key, value in properties['player_setting'].items():
            setattr(self, key, value)

    def shoot(self, **kwargs):
        # 如果玩家想要发射子弹
        if self.want_to_shoot:
            # 已经发射过，将其设为False
            self.want_to_shoot = False
            # 假设我们已经设置了开火冷却时间
            assert self.fire_cool_down_frame is not None
            # 如果距离上一次开火已经过了冷却时间
            if self.last_fire > self.fire_cool_down_frame:
                # 进行下一次开火
                self.last_fire = 0
                # 生成一个子弹
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
                        'damage': 4 * self.damage_factor,
                        'belonging': self
                    },
                )
                # 初始化子弹的移动
                temp.init_shoot_move((0, -5))
                # 返回是否生成了子弹，已经生成的子弹对象
                return True, temp
        # 如果没有开火，就将冷却帧+1
        self.last_fire += 1
        # 返回没有生成子弹的表示
        return False, None

    def set_target(self, target):
        """
        为自身的防卫激光设置开火目标

        :param target: 需要攻击的敌机对象
        :return:
        """
        for laser in self.defense_laser:
            laser.set_target(target)

    def update(self):
        """
        根系自身位置以及防卫激光的状态

        :return:
        """
        super().update()
        for laser in self.defense_laser:
            laser.update()

    def draw_self(self, window):
        """
        在window上绘制自身

        :param window: 需要绘制的pygame surface对象
        :return:
        """
        # 画飞机本体
        super().draw_self(window)
        # 画防卫激光
        for laser in self.defense_laser:
            laser.draw_self(window)


class Player2(Player):
    """
    不同的防卫激光布置模式
    """

    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         player_setting=properties['player_setting'], )
        self.defense_laser = [
            DefenseLaser(self, offset=(-15, 30)),
            DefenseLaser(self, offset=(15, 30)),
            DefenseLaser(self, offset=(0, -10)),
        ]


class Player3(Player):
    """
    不同的防卫激光布置模式
    """

    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         player_setting=properties['player_setting'], )
        self.defense_laser = [
            DefenseLaser(self)
        ]
