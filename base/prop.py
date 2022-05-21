from base.game_object import GameObject
from base.game import Game
from enum import Enum


class PropType(Enum):
    HEALTH_UP = 1
    DAMAGE_UP = 2
    SHOOTING_SPEED_UP = 3


class Prop(GameObject):
    def __init__(self, **kwargs):
        super().__init__(
            basic_setting=kwargs['basic_setting']
            )

        self.type = None
        for key, value in kwargs['prop_setting']:
            setattr(self, key, value)

        # 调用时type属性应该为一个数值

    def init_move(self, vector):
        self.vx = vector[0]
        self.vy = vector[1]


