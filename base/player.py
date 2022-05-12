import pygame
from plane import Plane


class Player(Plane):
    def __init__(self, x,y, vx,vy,texture,**properties):
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

    def change_pos(self, vector):
        self.x+=vector[0]
        self.y+=vector[1]

    def get_pos(self):
        return self.x,self.y

    def draw_self(self, window):
        super(Player, self).draw_self(window)


