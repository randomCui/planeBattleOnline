import pygame.draw

from inertia_object import InertiaObject
from bullet import BulletSimple
from shared_lib import t


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
        self.last_fire = 0

        for key, value in properties['plane_setting'].items():
            setattr(self, key, value)

        self._old_health_ = self.health
        self._health_bar_width_ = max(50, self.width * 0.8)
        self._health_bar_bottom_color_ = pygame.color.Color(130, 0, 0)
        self._health_bar_top_color_ = pygame.color.Color(0, 200, 0)
        self._health_bar_x_offset_ = self.width/2-self._health_bar_width_ / 2
        self._health_bar_y_offset = -20

    def hit(self, amount=1):
        assert self.health is not None
        self.health -= amount

    def init_move(self, speed_vector):
        self.vx, self.vy = speed_vector

    def shoot(self, **kwargs):
        assert self.fire_cool_down_frame is not None
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0
            temp = BulletSimple(
                basic_setting={
                    'x': self.get_center()[0] - t.lib['BLUE_LASER'].get_size()[0] / 2,
                    'y': self.get_center()[1] - t.lib['BLUE_LASER'].get_size()[1] / 2,
                    'size': t.lib['BLUE_LASER'].get_size(),
                    'texture_name': 'BLUE_LASER',
                },
                inertia_setting={
                    'max_speed': 5,
                },
                bullet_setting={
                    'damage': 4,
                },
            )
            temp.init_shoot_move((0, 0))
            return True, temp
        else:
            self.last_fire += 1
            return False, None

    def draw_self(self, window):
        super().draw_self(window)
        # 下面为显示血条的逻辑
        health_percent = self.health / self._old_health_
        # 显示血量全长
        pygame.draw.rect(window,
                         self._health_bar_bottom_color_,
                         pygame.rect.Rect(
                             self.x + self._health_bar_x_offset_,
                             self.y + self._health_bar_y_offset,
                             self._health_bar_width_,
                             10
                            )
                         )
        pygame.draw.rect(window,
                         self._health_bar_top_color_,
                         pygame.rect.Rect(
                             self.x+self._health_bar_x_offset_,
                             self.y + self._health_bar_y_offset,
                             self._health_bar_width_*health_percent,
                             10
                            )
                         )
