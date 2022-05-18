from game_object import GameObject
import animate_lib as lib


class Animation(GameObject):
    def __init__(self, center_pos,speed_vector,img_sequence_name):
        super(Animation, self).__init__(
            basic_setting={
                'x': center_pos[0] - lib.animate[img_sequence_name][0].get_width() / 2,
                'y': center_pos[1] - lib.animate[img_sequence_name][0].get_height() / 2,
                'vx':speed_vector[0],
                'vy':speed_vector[1],
                'size': lib.animate[img_sequence_name][0].get_size(),
            }
        )
        # 记录动画放到第几张图片
        self.counter = 0
        # 每隔几帧更新一次动画
        self.frame_per_update = 5
        self.second_counter = 0
        self.is_finish = False
        self.img_sequence_name = img_sequence_name
        self.length = len(lib.animate[self.img_sequence_name])

    def update(self):
        self.second_counter += 1
        if self.second_counter // self.frame_per_update > 0:
            self.second_counter = 0
            self.counter += 1

    def draw_self(self, window):
        super().init_texture(lib.animate[self.img_sequence_name][self.counter])
        super().draw_self(window)




