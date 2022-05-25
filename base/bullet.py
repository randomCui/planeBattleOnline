from inertia_object import InertiaObject
from util import distance_between, vector_angle_from_y


class Bullet(InertiaObject):
    def __init__(self, **properties):
        # 将参数传递给上一级
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         )
        # 子弹伤害
        self.damage = None
        # 子弹自身的动画(在游戏中未使用)
        self.animation_list = []
        # 判断子弹是否被摧毁
        self.not_destroyed = True
        # 每颗子弹拥有自己的发射者，用于结算分数
        self.belonging = None

        # 将自身的参数填入类中
        for key, value in properties['bullet_setting'].items():
            setattr(self, key, value)

    def get_damage(self):
        # 获得伤害数值
        if self.not_destroyed:
            return self.damage

    def init_shoot_move(self, speed_vector):
        # 初始化运动
        self.vx = speed_vector[0]
        self.vy = speed_vector[1]

    def update(self):
        # 更新位置信息
        super(Bullet, self).update()


class BulletSimple(Bullet):
    """
    简单子弹就是子弹类
    """
    pass


class BulletAiming(Bullet):
    """
    带瞄准的子弹有额外的逻辑
    """

    def __init__(self, **properties):
        # 子弹瞄准的目标
        self.target = None
        # 将参数填入上一级
        super(BulletAiming, self).__init__(basic_setting=properties['basic_setting'],
                                           inertia_setting=properties['inertia_setting'],
                                           bullet_setting=properties['bullet_setting']
                                           )
        # 假设目标坐标已经被设置好了
        assert self.target is not None
        # 计算射击的向量，距离等参数
        target_vector = self.target[0] - self.get_center()[0], self.target[1] - self.get_center()[1]
        distance = distance_between(self.target, self.get_center())
        # 根据计算得到的数据初始化子弹运动
        self.vx = self.max_speed * (target_vector[0] / distance)
        self.vy = self.max_speed * (target_vector[1] / distance)
        self.angle = vector_angle_from_y(target_vector)
