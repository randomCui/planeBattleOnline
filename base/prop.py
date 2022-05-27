from enum import Enum

from base.game_object import GameObject


class PropType(Enum):
    """
    枚举类型，表示不同的道具种类
    """
    HEALTH_UP = 1
    BULLET_UP = 2
    SHOOTING_SPEED_UP = 3


class Prop(GameObject):
    def __init__(self, **kwargs):
        super().__init__(
            basic_setting=kwargs['basic_setting']
        )

        self.type = None
        # 每个道具再屏幕上应该的存在时间(以帧计)
        self.designate_keep_time = None
        # 该道具已经存活的时间
        self.keep_time = 0

        # 将传入的参数逐个设置到类中
        for key, value in kwargs['prop_setting'].items():
            setattr(self, key, value)

        # 调用时type属性应该为一个数值

    def init_move(self, vector):
        # 设置对象的移动
        self.vx = vector[0]
        self.vy = vector[1]

    def update(self):
        # 更新游戏对象的位置
        super().update()
        # 将已经存活帧数+1
        self.keep_time += 1
