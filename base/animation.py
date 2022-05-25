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
        # 用于分频的计数器
        self.second_counter = 0
        # 动画是否已经播放完成
        self.is_finish = False
        # 动画的各个帧的序列
        self.img_sequence_name = img_sequence_name
        # 动画的总帧数长度
        self.length = len(lib.animate[self.img_sequence_name]) - 1

    def update(self):
        # 分频计数器+1
        self.second_counter += 1
        # 如果分频到了每隔几帧更新动画的情况
        if self.second_counter // self.frame_per_update > 0:
            # 分频计数器=0
            self.second_counter = 0
            # 防止动画越界
            self.counter = min(self.counter + 1, self.length)

    def draw_self(self, window):
        # 显示图片
        super().init_texture(lib.animate[self.img_sequence_name][self.counter])
        super().draw_self(window)




