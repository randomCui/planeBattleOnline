import pygame
from plane import Plane
from math import pow, sqrt


class Player(Plane):
    def __init__(self, x,y,texture,**properties):
        """
        初始化玩家对象

        :param x: 初始时对象的x位置
        :param y: 初始时对象的y位置
        :param vx: 初始时对象的x方向速度
        :param vy: 初始时对象的y方向速度
        :param properties: 其余玩家对象需要的各种属性，例如生命值，技能量等
        """
        super().__init__(x,y)
        self.texture = texture
        for key, value in properties.items():
            setattr(self,key,value)
        super().init_texture(self.texture)

        self.speed = 0

    def change_pos(self, vector):
        self.normalize_move_vector(vector)

    def get_pos(self):
        return self.x,self.y

    def normalize_move_vector(self,vector):
        if vector == (0,0):
            return
        hypotenuse = sqrt(pow(vector[0]+self.vx, 2) + pow(vector[1]+self.vy, 2))
        self.vx = vector[0]+self.vx / hypotenuse
        self.vy = vector[1]+self.vy / hypotenuse

        print(hypotenuse)
        assert hasattr(self,'max_speed')
        new_speed = hypotenuse
        if new_speed > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = new_speed


    def update(self):
        self.x += self.speed * self.vx
        self.y += self.speed * self.vy

    def draw_self(self, window):
        super(Player, self).draw_self(window)


