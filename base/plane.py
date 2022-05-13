import sys

sys.path.append('/')


class Plane:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # 设置生命值，移动速度等等内容
        self.width = 0
        self.height = 0
        self.rect = None
        self.texture = None

    def init_texture(self, texture):
        if texture is not None:
            self.texture = texture
            self.height = texture.get_height()
            self.width = texture.get_width()
        else:
            raise ValueError("Texture cannot be None")

    def draw_self(self, window):
        """
        将游戏中的飞行物体直接画在对应的窗口中

        :param window: 需要显示到的窗口
        :return:
        """
        # 假设在显示图形之前图像已经被初始化完成
        assert self.texture is not None
        window.blit(self.texture, (self.x, self.y))

    def __str__(self):
        """
        将游戏对象状态转为字符串，便于调试

        :return: 游戏对象的字符串
        """
        return format("Pos:(%.2f)(%2.f),Vector:(%.2f)(%.2f)" % (self.x, self.y, self.vx, self.vy))
