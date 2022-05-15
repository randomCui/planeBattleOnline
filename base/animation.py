from game_object import GameObject


class Animation(GameObject):
    def __init__(self, pos,speed_vector,img_sequence_name):
        super(Animation, self).__init__(
            basic_setting={
                'x':pos[0],
                'y':pos[1],
                'vx':speed_vector[0],
                'vy':speed_vector[1],
            }
        )
        # 记录动画放到第几张图片
        self.counter = 0
        # 每隔几帧更新一次动画
        self.frame_per_update = 1
        self.is_finish = False
        self.img_sequence_name = img_sequence_name
        self.length = len(img_sequence)



