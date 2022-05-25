from bullet import Bullet
from util import adjust_move_vector, vector_from_A_to_B, distance_between


class Missile(Bullet):
    """
    导弹对象
    """
    def __init__(self, **properties):
        # 将参数传递给上一级
        super().__init__(
            basic_setting=properties['basic_setting'],
            inertia_setting=properties['inertia_setting'],
            bullet_setting=properties['missile_setting'],
        )
        # 因为导弹可以被拦截，因此有生命值
        self.health = 0
        self.target_object = properties['missile_setting']['target_object']
        # 导弹的动力段时间
        self.life_time = properties['missile_setting']['life_time']
        # 当导弹即将接近飞机的范围
        self.approach_threshold = 100
        # 阻尼系数
        self.dumper_factor = 0.99
        # 导弹在动力段还是滑行段
        self.fuel = True

    def update(self):
        # 更新追踪的向量
        self.update_tracking()
        # 更新位置
        super().update()

    def update_tracking(self):
        # 如果还在动力段，每次更新时都让导弹指向己方飞机的方向
        if self.fuel:
            # 动力段剩余时间时间-1
            self.life_time -= 1
            move_vector = vector_from_A_to_B(self.get_center(), self.target_object.get_center())
            move_vector = adjust_move_vector(move_vector)
            self.change_pos(move_vector)
            if distance_between(self.get_center(), self.target_object.get_center()) < self.approach_threshold:
                self.damping()

    def hit(self, amount):
        # 导弹被激光防卫系统击中
        self.health -= amount
        return self.health <= 0
