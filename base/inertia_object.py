import pygame
from game_object import GameObject
from math import pow, sqrt


class InertiaObject(GameObject):
    dumper_factor = 0.95

    def __init__(self, **properties):
        # 将参数传递给上一级
        super().__init__(basic_setting=properties['basic_setting'])
        self.max_speed = None
        # 获取自己的参数
        for key, value in properties['inertia_setting'].items():
            setattr(self, key, value)

    def init_texture(self, texture):
        super().init_texture(texture)

    def change_pos(self, vector):
        # 将传入的方向向量标准化后进行改变
        self.normalize_move_vector(vector)

    def get_pos(self):
        return self.x, self.y

    def set_speed_vector(self, vector):
        # 直接设置对象的速度向量
        self.vx = vector[0]
        self.vy = vector[1]

    def normalize_move_vector(self, vector):
        # 标准化方向向量
        if vector == (0, 0):
            return
        hypotenuse = sqrt(pow(vector[0] + self.vx, 2) + pow(vector[1] + self.vy, 2))
        self.vx += vector[0]
        self.vy += vector[1]

        assert self.max_speed is not None
        # 如果斜边过大，说明物体运动超速了，需要限制飞机的运动速度
        if hypotenuse > self.max_speed:
            self.vx *= (self.max_speed / hypotenuse)
            self.vy *= (self.max_speed / hypotenuse)

    def damping(self):
        # 进行阻尼减速
        self.vx *= self.dumper_factor
        self.vy *= self.dumper_factor

    def update(self):
        # 更新游戏对象位置
        self.x += self.vx
        self.y += self.vy

    def draw_self(self, window):
        super(InertiaObject, self).draw_self(window)

    def set_pos(self, pos):
        # 直接改变对象位置
        self.x = pos[0]
        self.y = pos[1]
