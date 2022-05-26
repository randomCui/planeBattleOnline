import pygame

from base.util import distance_between, vector_from_A_to_B, calculate_end_point


class DefenseLaser:
    def __init__(self, attached_obj, **kwargs):
        # 防卫激光从属的对象
        self.attached_obj = attached_obj
        # 在从属对象上的偏移量(从中心点算)
        self.offset = (0, 0)
        # 激光的开始点
        self.start = attached_obj.x, attached_obj.y
        # 激光的结束点
        self.end = self.start
        # 激光的长度
        self.laser_length = 0
        # 瞄准的对象的引用
        self.target_obj = None
        # 下一个目标
        self.next_target = None
        # 激光在展开还是收回
        self.is_extending = False
        # 防卫激光目前是否在切换下一个目标
        self.changing_target = False

        # 以下为默认值
        # 最大射程
        self.max_range = 300
        # 展开/收回速度
        self.extend_speed_per_frame = 10

        # 将需要的参数填入类内
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_target(self, target):
        # 如果新传入的目标不是当前目标
        if self.target_obj is not target:
            # 将目标转换标志设为真
            self.changing_target = True
            # 切换瞄准目标
            self.target_obj = target

    def update(self):
        # 计算激光在屏幕上绝对位置的起始点
        self.start = self.attached_obj.get_center()[0] + self.offset[0], \
                     self.attached_obj.get_center()[1] + self.offset[1]
        # 如果激光没有在转换目标的途中并且目标不为空，就进入正常追踪模式
        if not self.changing_target and self.target_obj is not None:
            # 计算激光和目标之间的距离
            distance = distance_between(self.start, self.target_obj.get_center())
            # 语句等价于 self.is_extending = distance < self.max_range
            # 如果距离超过射程，让激光收回，进入射程就伸展
            if distance < self.max_range:
                self.is_extending = True
            else:
                self.is_extending = False

            if self.is_extending is True:
                # 如果在伸展，每次更新都给激光的长度加上展开速度，但是不能超过最大射程
                self.laser_length = min(self.max_range, self.laser_length + self.extend_speed_per_frame)
            else:
                # 如果在收回，收回的最小值只能到0
                self.laser_length = max(0, self.laser_length - self.extend_speed_per_frame)

            # 计算由激光发射点到目标的向量
            shoot_vector = vector_from_A_to_B(self.start, self.target_obj.get_center())
            # 计算在当前激光长度下激光能打到哪里
            end_vector = calculate_end_point(shoot_vector, self.laser_length)
            # 加上偏移量形成在屏幕上的绝对坐标
            self.end = end_vector[0] + self.start[0], end_vector[1] + self.start[1]

            # 如果已经命中到目标附近，就开始对导弹造成伤害
            if distance_between(self.end, self.target_obj.get_center()) < 3:
                self.target_obj.hit(0.1)

        else:
            # 如果目标为空，或是在转换目标，就首先将激光回收
            if self.laser_retracted():
                self.changing_target = False

        if self.target_obj is not None:
            # 通过判断是否在最大射程内决定是否要开始展开防卫激光
            distance = distance_between(self.start, self.target_obj.get_center())
            # 如果切换目标，就要先收回激光再次展开
            if self.changing_target:
                if self.laser_retracted():
                    self.changing_target = False

            # 如果没有完全伸展就让其完全伸展
            else:
                # 语句等价于 self.is_extending = distance < self.max_range
                if distance < self.max_range:
                    self.is_extending = True
                else:
                    self.is_extending = False

                if self.is_extending is True:
                    self.laser_length = min(distance, self.laser_length + self.extend_speed_per_frame)
                else:
                    self.laser_length = max(0, self.laser_length - self.extend_speed_per_frame)

                shoot_vector = vector_from_A_to_B(self.start, self.target_obj.get_center())
                end_vector = calculate_end_point(shoot_vector, self.laser_length)
                self.end = end_vector[0] + self.start[0], end_vector[1] + self.start[1]
                if distance_between(self.end, self.target_obj.get_center()) < 10:
                    if self.target_obj.hit(0.1):
                        self.laser_length = 0
                        self.end = self.start
        else:
            self.laser_length = 0
            self.end = self.start

    def laser_retracted(self):
        # 如果激光已经完全收回，就返回真
        if self.laser_length == 0:
            return True
        # 不断给激光减去伸缩速度，但是不能小于0
        self.laser_length = max(0, self.laser_length - self.extend_speed_per_frame)
        # 从当前位置到目标的射击向量
        shoot_vector = vector_from_A_to_B(self.start, self.end)
        # 计算在当前长度下的终点位置
        end_vector = calculate_end_point(shoot_vector, self.laser_length)
        # 加上偏移量，形成屏幕上的绝对坐标
        self.end = end_vector[0] + self.start[0], end_vector[1] + self.start[1]
        # 再次判断是否完全收回
        return self.laser_length == 0

    def draw_self(self, window):
        # 激光就是一条线，因此直接划线即可
        pygame.draw.line(window, pygame.color.Color(80, 200, 246, 80), self.start, self.end, width=3)
