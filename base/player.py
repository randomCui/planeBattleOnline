import pygame
from plane import Plane
from math import pow, sqrt


class Player(Plane):
    dumper_factor = 0.95

    def __init__(self, x, y, width, height, properties={}):
        """
        初始化玩家对象

        :param x: 初始时对象的x位置
        :param y: 初始时对象的y位置
        :param vx: 初始时对象的x方向速度
        :param vy: 初始时对象的y方向速度
        :param properties: 其余玩家对象需要的各种属性，例如生命值，技能量等
        """
        super().__init__(x, y)
        self.texture = None
        for key, value in properties.items():
            setattr(self, key, value)
        self.height = height
        self.width = width

    def init_texture(self, texture):
        super().init_texture(texture)

    def change_pos(self, vector):
        self.normalize_move_vector(vector)

    def get_pos(self):
        return self.x, self.y

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def set_speed_vector(self, vector):
        self.vx = vector[0]
        self.vy = vector[1]

    def normalize_move_vector(self, vector):
        if vector == (0, 0):
            return
        hypotenuse = sqrt(pow(vector[0] + self.vx, 2) + pow(vector[1] + self.vy, 2))
        self.vx += vector[0]
        self.vy += vector[1]
        # 如果斜边过大，说明物体运动超速了，需要限制飞机的运动速度
        if hypotenuse > self.max_speed:
            self.vx *= (self.max_speed / hypotenuse)
            self.vy *= (self.max_speed / hypotenuse)

    def dumper_once(self):
        self.vx *= self.dumper_factor
        self.vy *= self.dumper_factor

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw_self(self, window):
        super(Player, self).draw_self(window)
