import pygame.draw

from bullet import BulletSimple
from inertia_object import InertiaObject
from shared_lib import t


class Plane(InertiaObject):
    def __init__(self, **properties):
        """
        游戏中的飞机对象
        """
        # 将参数传递给上一级
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         )
        # 飞机对象的生命值
        self.health = None
        # 飞机上次开火
        self.last_fire = 0

        # 获取自己的属性
        for key, value in properties['plane_setting'].items():
            setattr(self, key, value)

        # 初始化生命值条的几何外形
        self._old_health_ = self.health
        self._health_bar_width_ = max(50, self.width * 0.8)
        self._health_bar_bottom_color_ = pygame.color.Color(130, 0, 0)
        self._health_bar_top_color_ = pygame.color.Color(0, 200, 0)
        self._health_bar_x_offset_ = self.width / 2 - self._health_bar_width_ / 2
        self._health_bar_y_offset = -20

    def hit(self, amount=1):
        # 假设飞机已经设置了health属性
        assert self.health is not None
        # 被击中后生命值被减掉
        self.health -= amount

    def init_move(self, speed_vector):
        # 初始化移动向量
        self.vx, self.vy = speed_vector

    def shoot(self, **kwargs):
        # 假设已经设置了开火冷却间隔
        assert self.fire_cool_down_frame is not None
        # 如果上一次开火已经大于了开火冷却时间
        if self.last_fire > self.fire_cool_down_frame:
            self.last_fire = 0
            # 生成一个新的子弹
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
            # 初始化子弹的移动
            temp.init_shoot_move((0, 0))
            # 返回子弹生成成功和生成出的子弹
            return True, temp
        else:
            # 如果没有成功，开过间隔时间+1
            self.last_fire += 1
            # 返回子弹生成失败
            return False, None

    def draw_self(self, window):
        # 调用基类的绘制自身的逻辑
        super().draw_self(window)
        # 下面为显示血条的逻辑
        health_percent = self.health / self._old_health_
        # 显示当前血量
        pygame.draw.rect(window,
                         self._health_bar_bottom_color_,
                         pygame.rect.Rect(
                             self.x + self._health_bar_x_offset_,
                             self.y + self._health_bar_y_offset,
                             self._health_bar_width_,
                             10
                         )
                         )
        # 显示总血量
        pygame.draw.rect(window,
                         self._health_bar_top_color_,
                         pygame.rect.Rect(
                             self.x + self._health_bar_x_offset_,
                             self.y + self._health_bar_y_offset,
                             self._health_bar_width_ * health_percent,
                             10
                         )
                         )
