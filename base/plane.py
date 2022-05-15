from inertia_object import InertiaObject


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

        for key, value in properties['plane_setting'].items():
            setattr(self, key, value)

    def hit(self, amount=1):
        assert self.health is not None
        self.health -= amount
        print(self.health)

    def init_move(self, speed_vector):
        self.vx, self.vy = speed_vector

    def shoot(self,**kwargs):
        pass
