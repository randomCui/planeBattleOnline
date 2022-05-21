from base.util import distance_between, vector_from_A_to_B, calculate_end_point
import pygame


class DefenseLaser:
    def __init__(self, attached_obj, **kwargs):
        self.attached_obj = attached_obj
        self.offset = (0, 0)
        self.start = attached_obj.x, attached_obj.y
        self.end = self.start
        self.laser_length = 0
        self.target_obj = None
        self.next_target = None
        self.is_extending = False
        self.changing_target = False
        # self.percent_extended = 0

        # 以下为默认值
        self.max_range = 300
        self.extend_speed_per_frame = 10

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_target(self, target):
        if self.target_obj is not target:
            self.changing_target = True
            self.target_obj = target

    def update(self):
        self.start = self.attached_obj.get_center()[0] + self.offset[0], self.attached_obj.get_center()[1] + \
                     self.offset[1]
        if not self.changing_target and self.target_obj is not None:
            distance = distance_between(self.start, self.target_obj.get_center())
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
                self.target_obj.hit(0.1)

        else:
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
        if self.laser_length == 0:
            return True
        self.laser_length = max(0, self.laser_length - self.extend_speed_per_frame)
        shoot_vector = vector_from_A_to_B(self.start, self.end)
        end_vector = calculate_end_point(shoot_vector, self.laser_length)
        self.end = end_vector[0] + self.start[0], end_vector[1] + self.start[1]
        return self.laser_length == 0

    def draw_self(self, window):
        pygame.draw.line(window, pygame.color.Color(80, 200, 246, 80), self.start, self.end, width=3)
